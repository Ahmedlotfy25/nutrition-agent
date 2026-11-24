

مساعد وجبات وسعرات حرارية بيستخدم **LLM Tool Calling** (يدعم OpenAI و Groq).
الـ LLM بيفهم طلب المستخدم، وبينادي على tools بتحسب الأرقام الغذائية بدقة من بيانات مكتوبة يدوي، فمفيش تخمين.


| Tool | الوظيفة |
|---|---|
| `search_recipes` | بحث في الوصفات حسب المكونات / النوع / السعرات |
| `get_ingredient_calories` | قيم غذائية لمكون بكمية معينة |
| `sum_meal_macros` | جمع قيم الوجبة ومقارنتها بالهدف اليومي |
| `calculate_daily_target` | حساب الاحتياج اليومي (Mifflin-St Jeor) |
| `convert_units` | تحويل حبة/كوب/معلقة لجرامات |


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

## هيكل المشروع
- `data.py`: بيانات المكونات والوصفات
- `tools.py`: الـ decorator `@tool` + دوال الـ tools (الـ schema بيتولّد أوتوماتيك من الـ type hints والـ docstring)
- `agent.py`: حلقة الـ agent (tool-calling loop)
- `main.py`: واجهة الـ CLI

> ⚠️ ده مش بديل لأخصائي تغذية.
