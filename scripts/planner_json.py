
"""
JSON-first Meal Planner
- Reads data/inventory.json and data/recipes.json
- Picks recipes for a period, preferring ingredient overlap
- Writes plan_YYYY-MM-DD.json and shopping_list_YYYY-MM-DD.csv into data/
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import date
import pandas as pd
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

@dataclass
class Ingredient:
    item: str
    quantity: float
    unit: str
    category: str

@dataclass
class Recipe:
    recipe_id: str
    title: str
    servings: int
    theme_tags: List[str]
    ingredients: List[Ingredient]
    instructions: str

def load_inventory() -> Dict[str, Dict[str, float]]:
    data = json.loads((DATA / "inventory.json").read_text(encoding="utf-8"))
    inv: Dict[str, Dict[str, float]] = {}
    for row in data.get("meats", []) + data.get("pantry", []):
        inv[row["item"]] = {"quantity": float(row["quantity"]), "unit": str(row["unit"])}
    return inv

def load_recipes() -> List[Recipe]:
    data = json.loads((DATA / "recipes.json").read_text(encoding="utf-8"))
    recs: List[Recipe] = []
    for r in data.get("recipes", []):
        ings = [Ingredient(**d) for d in r["ingredients"]]
        recs.append(Recipe(
            recipe_id=r["recipe_id"],
            title=r["title"],
            servings=int(r["servings"]),
            theme_tags=[t.strip() for t in r.get("theme_tags", [])],
            ingredients=ings,
            instructions=r.get("instructions", ""),
        ))
    return recs

def score_overlap(recipes: List[Recipe]) -> float:
    items = []
    for r in recipes:
        items.extend([ing.item for ing in r.ingredients])
    c = Counter(items)
    return sum((n - 1) for n in c.values() if n > 1)

def consolidate_needs(recipes: List[Recipe], inv: Dict[str, Dict[str, float]]) -> List[Tuple[str, float, str]]:
    need: Dict[Tuple[str, str], float] = {}
    for r in recipes:
        for ing in r.ingredients:
            key = (ing.item, ing.unit)
            need[key] = need.get(key, 0.0) + float(ing.quantity)
    rows = []
    for (item, unit), q in need.items():
        have = inv.get(item, {}).get("quantity", 0.0)
        net = max(0.0, q - have)
        if net > 0:
            rows.append((item, round(net, 2), unit))
    return rows

def choose_recipes(all_recipes: List[Recipe], target_meals: int, theme_hint: Optional[str] = None) -> List[Recipe]:
    candidates = all_recipes
    if theme_hint:
        th = theme_hint.lower()
        candidates = [r for r in all_recipes if any(th in t.lower() for t in r.theme_tags)] or all_recipes

    chosen: List[Recipe] = []
    remaining = candidates.copy()

    pop = Counter()
    for r in candidates:
        pop.update([ing.item for ing in r.ingredients])
    remaining.sort(key=lambda r: sum(pop[ing.item] for ing in r.ingredients), reverse=True)

    while remaining and len(chosen) < target_meals:
        if not chosen:
            chosen.append(remaining.pop(0))
            continue
        best_i = -1
        best_s = -1.0
        for i, r in enumerate(remaining):
            s = score_overlap(chosen + [r])
            if s > best_s:
                best_s = s
                best_i = i
        chosen.append(remaining.pop(best_i))
    return chosen

def plan(period_days: int = 4, meals_per_day: int = 1, theme_hint: Optional[str] = None):
    inv = load_inventory()
    recipes = load_recipes()
    target_meals = period_days * meals_per_day
    chosen = choose_recipes(recipes, target_meals, theme_hint=theme_hint)

    shopping = consolidate_needs(chosen, inv)

    stamp = date.today().isoformat()
    plan_json = {
        "date": stamp,
        "period_days": period_days,
        "meals_per_day": meals_per_day,
        "theme_hint": theme_hint,
        "recipes": [
            {
                "recipe_id": r.recipe_id,
                "title": r.title,
                "servings": r.servings,
                "ingredients": [ing.__dict__ for ing in r.ingredients],
                "instructions": r.instructions,
            }
            for r in chosen
        ],
    }
    (DATA / f"plan_{stamp}.json").write_text(json.dumps(plan_json, indent=2), encoding="utf-8")
    import pandas as pd
    pd.DataFrame(shopping, columns=["item", "quantity_needed", "unit"]).to_csv(DATA / f"shopping_list_{stamp}.csv", index=False)
    return chosen, shopping, plan_json

if __name__ == "__main__":
    chosen, shopping, plan_json = plan(period_days=4, meals_per_day=1, theme_hint="korean")
    print("Chosen:", [r.title for r in chosen])
    print("Shopping items:", len(shopping))
