"""الـ Tools: دوال بايثون عادية + decorator @tool بيسجّلها ويبني الـ schema أوتوماتيك.
ملاحظة: ماتستخدمش `from __future__ import annotations` هنا، لأن الـ decorator بيقرأ الـ type hints."""
import inspect
from typing import Literal, get_args, get_origin

from data import (ACTIVITY_MULTIPLIERS, ALIASES, DEFAULT_UNITS, GOAL_ADJUSTMENT,
                  INGREDIENTS, RECIPES, SPECIFIC_UNITS)


TOOL_FUNCTIONS = {}   
TOOLS_SCHEMA = []     

_TYPES = {str: "string", int: "integer", float: "number", bool: "boolean"}


def _to_schema(tp) -> dict:
    if get_origin(tp) is Literal:                  
        return {"type": "string", "enum": list(get_args(tp))}
    if get_origin(tp) is list:                     
        inner = get_args(tp)
        return {"type": "array", "items": _to_schema(inner[0]) if inner else {}}
    if tp is dict or get_origin(tp) is dict:
        return {"type": "object"}
    return {"type": _TYPES.get(tp, "string")}


def tool(func):
    """بيقرأ اسم الدالة والـ docstring والـ type hints ويبني منهم الـ schema ويسجّل الدالة."""
    props, required = {}, []
    for name, p in inspect.signature(func).parameters.items():
        props[name] = _to_schema(p.annotation)
        if p.default is inspect.Parameter.empty:   
            required.append(name)

    TOOLS_SCHEMA.append({"type": "function", "function": {
        "name": func.__name__,
        "description": inspect.getdoc(func),
        "parameters": {"type": "object", "properties": props, "required": required},
    }})
    TOOL_FUNCTIONS[func.__name__] = func
    return func


def _resolve(name: str):
    """يحوّل اسم المكون (عربي/إنجليزي) للمفتاح الأساسي، أو None لو مش موجود."""
    n = name.strip().lower()
    if n in INGREDIENTS:
        return n
    return ALIASES.get(n) or ALIASES.get(name.strip())



@tool
def get_ingredient_calories(ingredient: str, grams: float) -> dict:
    """يرجّع السعرات والبروتين والكارب والدهون لمكون واحد بكمية معينة بالجرام.
    ingredient: اسم المكون بالعربي أو الإنجليزي مثلاً 'فراخ' أو 'rice'."""
    key = _resolve(ingredient)
    if key is None:
        return {"error": f"المكون '{ingredient}' مش موجود في قاعدة البيانات.",
                "available": sorted(INGREDIENTS.keys())}
    per100 = INGREDIENTS[key]
    f = grams / 100
    return {
        "ingredient": key, "grams": grams,
        "calories": round(per100["calories"] * f, 1),
        "protein": round(per100["protein"] * f, 1),
        "carbs": round(per100["carbs"] * f, 1),
        "fat": round(per100["fat"] * f, 1),
    }


@tool
def sum_meal_macros(items: list[dict], daily_target_calories: float = None) -> dict:
    """يجمع القيم الغذائية لوجبة كاملة، ولو اتحدد هدف يومي بالسعرات يقارن بيه.
    items: قائمة مكونات، كل عنصر شكله {"ingredient": "فراخ", "grams": 150}."""
    total = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    breakdown, errors = [], []
    for it in items:
        r = get_ingredient_calories(it["ingredient"], it["grams"])
        if "error" in r:
            errors.append(r["error"])
            continue
        breakdown.append(r)
        for k in total:
            total[k] += r[k]
    total = {k: round(v, 1) for k, v in total.items()}
    result = {"total": total, "breakdown": breakdown}
    if errors:
        result["errors"] = errors
    if daily_target_calories:
        result["percent_of_daily_target"] = round(total["calories"] / daily_target_calories * 100, 1)
        result["remaining_calories"] = round(daily_target_calories - total["calories"], 1)
    return result


@tool
def search_recipes(ingredients: list[str] = None,
                   tag: Literal["breakfast", "lunch", "dinner", "snack", "high_protein",
                                "low_carb", "vegetarian", "budget"] = None,
                   max_calories: float = None) -> dict:
    """يدوّر في الوصفات المتاحة حسب المكونات اللي عند المستخدم، أو نوع الوجبة، أو حد أقصى للسعرات.
    ingredients: المكونات الموجودة عند المستخدم بالعربي أو الإنجليزي."""
    have = {_resolve(i) for i in (ingredients or [])} - {None}
    results = []
    for r in RECIPES:
        if tag and tag not in r["tags"]:
            continue
        macros = sum_meal_macros([{"ingredient": k, "grams": g} for k, g in r["ingredients"].items()])["total"]
        if max_calories and macros["calories"] > max_calories:
            continue
        needed = set(r["ingredients"])
        matched = needed & have
        if have and not matched:
            continue
        results.append({
            "name": r["name"], "tags": r["tags"], "ingredients_grams": r["ingredients"],
            "missing_ingredients": sorted(needed - have) if have else [],
            "match_score": len(matched), "macros": macros, "steps": r["steps"],
        })
    results.sort(key=lambda x: (-x["match_score"], len(x["missing_ingredients"])))
    return {"count": len(results), "recipes": results[:5]}


@tool
def calculate_daily_target(weight_kg: float, height_cm: float, age: int,
                           gender: Literal["male", "female"],
                           activity: Literal["sedentary", "light", "moderate", "active"],
                           goal: Literal["lose", "maintain", "gain"]) -> dict:
    """يحسب احتياج المستخدم اليومي من السعرات والبروتين والكارب والدهون (معادلة Mifflin-St Jeor)."""
    s = 5 if gender == "male" else -161
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + s
    tdee = bmr * ACTIVITY_MULTIPLIERS[activity]
    target = tdee + GOAL_ADJUSTMENT[goal]
    protein_g = weight_kg * 1.6
    fat_g = target * 0.25 / 9
    carbs_g = (target - protein_g * 4 - fat_g * 9) / 4
    return {
        "bmr": round(bmr), "tdee": round(tdee), "target_calories": round(target),
        "target_protein_g": round(protein_g), "target_fat_g": round(fat_g),
        "target_carbs_g": round(carbs_g),
    }


@tool
def convert_units(amount: float, from_unit: Literal["piece", "cup", "tbsp", "tsp", "g", "kg"],
                  ingredient: str = None) -> dict:
    """يحوّل كمية بوحدة (حبة/كوب/معلقة) لجرامات. استخدمه لما المستخدم مايقولش الكمية بالجرام."""
    unit = from_unit.strip().lower()
    key = _resolve(ingredient) if ingredient else None
    per_unit = (SPECIFIC_UNITS.get(key, {}).get(unit)) or DEFAULT_UNITS.get(unit)
    if per_unit is None:
        return {"error": f"الوحدة '{from_unit}' مش معروفة للمكون ده. جرّب: piece, cup, tbsp, tsp, g, kg"}
    return {"ingredient": key, "amount": amount, "unit": unit, "grams": round(amount * per_unit, 1)}
