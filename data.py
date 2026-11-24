"""كل البيانات يدوي. القيم لكل 100 جرام (تقريبية من جداول USDA)."""


INGREDIENTS = {
    "chicken_breast": {"calories": 165, "protein": 31.0, "carbs": 0.0,  "fat": 3.6},   # مطبوخ
    "beef_lean":      {"calories": 250, "protein": 26.0, "carbs": 0.0,  "fat": 15.0},  # مطبوخ
    "salmon":         {"calories": 206, "protein": 22.0, "carbs": 0.0,  "fat": 12.0},  # مطبوخ
    "tuna_canned":    {"calories": 116, "protein": 26.0, "carbs": 0.0,  "fat": 0.8},   # في مية
    "egg":            {"calories": 143, "protein": 12.6, "carbs": 0.7,  "fat": 9.5},
    "rice":           {"calories": 130, "protein": 2.7,  "carbs": 28.0, "fat": 0.3},   # مطبوخ
    "pasta":          {"calories": 158, "protein": 5.8,  "carbs": 31.0, "fat": 0.9},   # مطبوخ
    "bread_baladi":   {"calories": 270, "protein": 9.0,  "carbs": 55.0, "fat": 1.5},
    "oats":           {"calories": 389, "protein": 16.9, "carbs": 66.0, "fat": 6.9},
    "potato":         {"calories": 87,  "protein": 1.9,  "carbs": 20.0, "fat": 0.1},   # مسلوق
    "fava_beans":     {"calories": 110, "protein": 7.6,  "carbs": 19.6, "fat": 0.4},   # فول مطبوخ
    "lentils":        {"calories": 116, "protein": 9.0,  "carbs": 20.0, "fat": 0.4},   # مطبوخ
    "chickpeas":      {"calories": 164, "protein": 8.9,  "carbs": 27.4, "fat": 2.6},   # مطبوخ
    "milk":           {"calories": 61,  "protein": 3.2,  "carbs": 4.8,  "fat": 3.3},
    "yogurt":         {"calories": 61,  "protein": 3.5,  "carbs": 4.7,  "fat": 3.3},
    "white_cheese":   {"calories": 264, "protein": 14.0, "carbs": 4.0,  "fat": 21.0},
    "tomato":         {"calories": 18,  "protein": 0.9,  "carbs": 3.9,  "fat": 0.2},
    "cucumber":       {"calories": 15,  "protein": 0.7,  "carbs": 3.6,  "fat": 0.1},
    "onion":          {"calories": 40,  "protein": 1.1,  "carbs": 9.3,  "fat": 0.1},
    "spinach":        {"calories": 23,  "protein": 2.9,  "carbs": 3.6,  "fat": 0.4},
    "broccoli":       {"calories": 34,  "protein": 2.8,  "carbs": 6.6,  "fat": 0.4},
    "banana":         {"calories": 89,  "protein": 1.1,  "carbs": 23.0, "fat": 0.3},
    "olive_oil":      {"calories": 884, "protein": 0.0,  "carbs": 0.0,  "fat": 100.0},
    "almonds":        {"calories": 579, "protein": 21.0, "carbs": 22.0, "fat": 50.0},
    "tahini":         {"calories": 595, "protein": 17.0, "carbs": 21.0, "fat": 54.0},
    "honey":          {"calories": 304, "protein": 0.3,  "carbs": 82.0, "fat": 0.0},
}


ALIASES = {
    "فراخ": "chicken_breast", "صدور فراخ": "chicken_breast", "chicken": "chicken_breast",
    "لحمة": "beef_lean", "لحم": "beef_lean", "beef": "beef_lean",
    "سلمون": "salmon", "سالمون": "salmon",
    "تونة": "tuna_canned", "tuna": "tuna_canned",
    "بيض": "egg", "بيضة": "egg", "eggs": "egg",
    "رز": "rice", "أرز": "rice",
    "مكرونة": "pasta", "مكرونه": "pasta",
    "عيش": "bread_baladi", "عيش بلدي": "bread_baladi", "bread": "bread_baladi",
    "شوفان": "oats",
    "بطاطس": "potato", "بطاطا": "potato",
    "فول": "fava_beans", "foul": "fava_beans",
    "عدس": "lentils",
    "حمص": "chickpeas",
    "لبن": "milk", "حليب": "milk",
    "زبادي": "yogurt",
    "جبنة": "white_cheese", "جبنة بيضاء": "white_cheese", "جبنه": "white_cheese", "cheese": "white_cheese",
    "طماطم": "tomato", "طماطة": "tomato", "tomatoes": "tomato",
    "خيار": "cucumber",
    "بصل": "onion",
    "سبانخ": "spinach",
    "بروكلي": "broccoli",
    "موز": "banana",
    "زيت زيتون": "olive_oil", "زيت": "olive_oil",
    "لوز": "almonds",
    "طحينة": "tahini", "طحينه": "tahini",
    "عسل": "honey",
}


DEFAULT_UNITS = {"g": 1, "gram": 1, "kg": 1000, "tbsp": 15, "tsp": 5, "cup": 240}


SPECIFIC_UNITS = {
    "egg":          {"piece": 50},
    "bread_baladi": {"piece": 90, "loaf": 90},
    "banana":       {"piece": 120},
    "tomato":       {"piece": 120},
    "cucumber":     {"piece": 100},
    "potato":       {"piece": 170},
    "onion":        {"piece": 110},
    "rice":         {"cup": 160},
    "pasta":        {"cup": 140},
    "oats":         {"cup": 90, "tbsp": 7},
    "olive_oil":    {"tbsp": 14, "tsp": 5},
    "honey":        {"tbsp": 21, "tsp": 7},
    "tahini":       {"tbsp": 15},
    "lentils":      {"cup": 200},
    "fava_beans":   {"cup": 170},
    "milk":         {"cup": 245},
    "yogurt":       {"cup": 245},
}

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,    # قليل الحركة
    "light": 1.375,      # تمرين 1-3 أيام
    "moderate": 1.55,    # تمرين 3-5 أيام
    "active": 1.725,     # تمرين 6-7 أيام
}

GOAL_ADJUSTMENT = {"lose": -500, "maintain": 0, "gain": 300}


RECIPES = [
    {
        "name": "فراخ مشوية مع رز",
        "tags": ["high_protein", "lunch"],
        "ingredients": {"chicken_breast": 150, "rice": 150, "tomato": 100, "olive_oil": 5},
        "steps": "تبّل الفراخ وتشويها، تسلق الرز، وتقدمهم مع سلطة طماطم بزيت الزيتون.",
    },
    {
        "name": "فول بالطحينة وبيض",
        "tags": ["breakfast", "high_protein", "budget"],
        "ingredients": {"fava_beans": 200, "egg": 100, "tahini": 15, "bread_baladi": 90, "olive_oil": 5},
        "steps": "سخّن الفول وزوّد الطحينة وزيت الزيتون، واسلق البيض، وقدمهم مع العيش.",
    },
    {
        "name": "شوربة عدس",
        "tags": ["vegetarian", "budget", "dinner"],
        "ingredients": {"lentils": 250, "onion": 50, "olive_oil": 5},
        "steps": "اسلق العدس مع البصل واضرب الشوربة في الخلاط، وزوّد زيت الزيتون.",
    },
    {
        "name": "سلطة تونة",
        "tags": ["high_protein", "low_carb", "dinner"],
        "ingredients": {"tuna_canned": 120, "tomato": 120, "cucumber": 100, "olive_oil": 10},
        "steps": "قطّع الخضار وزوّد التونة وزيت الزيتون وقدمها فوراً.",
    },
    {
        "name": "شوفان بالموز واللوز",
        "tags": ["breakfast", "vegetarian"],
        "ingredients": {"oats": 50, "milk": 200, "banana": 120, "almonds": 15, "honey": 10},
        "steps": "اطبخ الشوفان مع اللبن 5 دقايق، وزوّد الموز واللوز والعسل.",
    },
    {
        "name": "مكرونة بالفراخ والبروكلي",
        "tags": ["high_protein", "lunch"],
        "ingredients": {"pasta": 200, "chicken_breast": 120, "broccoli": 100, "olive_oil": 10},
        "steps": "اسلق المكرونة والبروكلي، وسوّتي الفراخ، وقلّبهم كلهم بزيت الزيتون.",
    },
    {
        "name": "سلمون مشوي مع بطاطس",
        "tags": ["high_protein", "dinner"],
        "ingredients": {"salmon": 150, "potato": 200, "spinach": 80, "olive_oil": 5},
        "steps": "اشوي السلمون، واسلق البطاطس، وسوتي السبانخ وقدمهم مع بعض.",
    },
    {
        "name": "أومليت سبانخ وجبنة",
        "tags": ["breakfast", "vegetarian", "low_carb"],
        "ingredients": {"egg": 150, "spinach": 60, "white_cheese": 40, "olive_oil": 5},
        "steps": "اخفق البيض، زوّد السبانخ والجبنة، وسوّيه على نار هادية.",
    },
    {
        "name": "حمص بالطحينة وخيار",
        "tags": ["vegetarian", "budget", "snack"],
        "ingredients": {"chickpeas": 150, "tahini": 20, "cucumber": 100, "bread_baladi": 45},
        "steps": "اهرس الحمص مع الطحينة وقدمه مع الخيار والعيش.",
    },
]
