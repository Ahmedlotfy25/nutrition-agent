

A meal and calorie assistant using LLM Tool Calling (supports OpenAI and Groq).
The LLM understands the user's request and calls tools that calculate nutritional numbers accurately from manually written data, so there is no guesswork.

| Tool | Function |
|---|---|
| `search_recipes` |Search recipes by ingredients / type / calories|
| `get_ingredient_calories` | Nutritional values for an ingredient with a specific quantity |
| `sum_meal_macros` | Sum meal values and compare them to the daily target |
| `calculate_daily_target` | Calculate daily needs (Mifflin-St Jeor) |
| `convert_units` | Convert piece/cup/spoon to grams |


```bash
git clone <your-repo-url> && cd nutrition-agent
python -m venv venv && source venv/bin/activate   
pip install -r requirements.txt
cp .env.example .env    
python main.py
```


```bash
python test_tools.py
```

## Project structure
data.py: Ingredients and recipes data

tools.py: The @tool decorator + tool functions (the schema is automatically generated from type hints and docstrings)

agent.py: The agent loop (tool-calling loop)

main.py: CLI interface

⚠️ This is not a substitute for a nutritionist.

> ⚠️ ده مش بديل لأخصائي تغذية.
