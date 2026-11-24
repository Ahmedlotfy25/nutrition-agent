import json
import os
from openai import OpenAI
from tools import TOOL_FUNCTIONS, TOOLS_SCHEMA

SYSTEM_PROMPT = """أنت مساعد تغذية بتتكلم بالعامية المصرية.
القواعد:
1. ممنوع تذكر أي رقم غذائي إلا من نتيجة tool، ماتخمنش أبداً.
2. لو الكمية بحبة/كوب/معلقة استخدم convert_units، ولو المستخدم ماحددش هدفه استخدم calculate_daily_target.
3. لو مكون مش موجود في قاعدة البيانات قول كده بصراحة.

شكل الرد (إلزامي):
- جاوب في سطر واحد قصير فقط، من غير قوائم ولا عناوين ولا فقرات.
- بعد السطر، في سطر جديد، اكتب "💡 نصيحة:" وبعدها نصيحة غذائية قصيرة مناسبة لسؤال المستخدم.
- مفيش أي كلام بعد النصيحة."""

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
        return "وصلت للحد الأقصى من الخطوات. جرّب تسأل بشكل أبسط."
