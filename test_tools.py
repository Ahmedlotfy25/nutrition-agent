"""اختبارات للـ tools من غير API. شغّلها بـ: python test_tools.py"""
from tools import *

def test_calories():
    r = get_ingredient_calories("فراخ", 200)
    assert r["calories"] == 330 and r["protein"] == 62

def test_unknown():
    assert "error" in get_ingredient_calories("شوكولاتة", 50)

def test_sum():
    r = sum_meal_macros([{"ingredient": "rice", "grams": 100}, {"ingredient": "egg", "grams": 100}], 2000)
    assert r["total"]["calories"] == 273 and r["remaining_calories"] == 1727

def test_target():
    r = calculate_daily_target(80, 180, 25, "male", "moderate", "maintain")
    assert 2700 < r["target_calories"] < 2800

def test_units():
    assert convert_units(2, "piece", "بيض")["grams"] == 100

def test_search():
    r = search_recipes(["فراخ", "رز"])
    assert r["recipes"][0]["name"] == "فراخ مشوية مع رز"

def test_decorator_registry():
    assert set(TOOL_FUNCTIONS) == {"get_ingredient_calories", "sum_meal_macros", "search_recipes",
                                   "calculate_daily_target", "convert_units"}
    assert len(TOOLS_SCHEMA) == 5

def test_decorator_schema():
    sch = {t["function"]["name"]: t["function"] for t in TOOLS_SCHEMA}
    p = sch["calculate_daily_target"]["parameters"]
    assert p["properties"]["activity"]["enum"] == ["sedentary", "light", "moderate", "active"]
    assert p["required"] == ["weight_kg", "height_cm", "age", "gender", "activity", "goal"]
    sm = sch["sum_meal_macros"]["parameters"]
    assert sm["required"] == ["items"] and sm["properties"]["items"]["type"] == "array"
    assert sch["search_recipes"]["parameters"]["required"] == []
    assert sch["get_ingredient_calories"]["description"]

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f(); print("✅", n)
