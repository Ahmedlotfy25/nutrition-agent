import json
import os
from openai import OpenAI
from tools import TOOL_FUNCTIONS, TOOLS_SCHEMA

SYSTEM_PROMPT = """You are a nutrition assistant who speaks in Egyptian colloquial dialect.
Rules:
1. Do not mention any nutritional number except from a tool result; never guess.
2. If the quantity is in pieces/cups/spoons, use convert_units, and if the user hasn't specified their goal, use calculate_daily_target.
3. If an ingredient is not in the database, say so honestly.

Response format (mandatory):
- Answer in a single short line only, with no lists, headings, or paragraphs.
- After that line, on a new line, write "💡 Tip:" followed by a short nutritional tip suitable for the user's question.
- No text after the tip."""

PROVIDERS = {
    "openai": {"base_url": None, "key_env": "OPENAI_API_KEY", "model_env": "OPENAI_MODEL", "default_model": "gpt-4o"},
    "groq": {"base_url": "https://api.groq.com/openai/v1", "key_env": "GROQ_API_KEY",
             "model_env": "GROQ_MODEL", "default_model": "llama-3.3-70b-versatile"},
}


class NutritionAgent:
    def __init__(self, provider: str = "groq", max_steps: int = 6):
        cfg = PROVIDERS[provider]
        self.client = OpenAI(api_key=os.environ[cfg["key_env"]], base_url=cfg["base_url"])
        self.model = os.getenv(cfg["model_env"], cfg["default_model"])
        self.max_steps = max_steps
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def _run_tool(self, name: str, args: dict) -> str:
        fn = TOOL_FUNCTIONS.get(name)
        if fn is None:
            return json.dumps({"error": f"tool '{name}' مش موجود"}, ensure_ascii=False)
        try:
            return json.dumps(fn(**args), ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

    def chat(self, user_message: str, verbose: bool = True) -> str:
        self.messages.append({"role": "user", "content": user_message})
        for _ in range(self.max_steps):
            resp = self.client.chat.completions.create(
                model=self.model, messages=self.messages,
                tools=TOOLS_SCHEMA, tool_choice="auto", temperature=0.2,
            )
            msg = resp.choices[0].message
            self.messages.append(msg)

            if not msg.tool_calls:          
                return msg.content

            for call in msg.tool_calls:    
                try:
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                if verbose:
                    print(f"  🔧 {call.function.name}({args})")
                self.messages.append({
                    "role": "tool", "tool_call_id": call.id,
                    "content": self._run_tool(call.function.name, args),
                })
      return "You've reached the maximum number of steps. Try asking in a simpler way."
