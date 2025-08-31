
"""
merge_recipes.py
- Append one or more recipes to data/recipes.json, unique by recipe_id.
Usage:
    python merge_recipes.py path/to/new_recipes.json
Where new_recipes.json can be either:
    {"recipes": [ ... ]}  OR  a single recipe object {...}
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CATALOG = DATA / "recipes.json"

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def main():
    if len(sys.argv) != 2:
        print("Usage: python merge_recipes.py path/to/new_recipes.json")
        sys.exit(1)
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"Not found: {src}")
        sys.exit(1)

    incoming = load_json(src)
    catalog = load_json(CATALOG)

    if isinstance(incoming, dict) and "recipes" in incoming:
        new_items = incoming["recipes"]
    else:
        new_items = [incoming]

    by_id = {r["recipe_id"]: r for r in catalog.get("recipes", [])}
    added, updated = 0, 0
    for r in new_items:
        rid = r["recipe_id"]
        if rid in by_id:
            by_id[rid] = r
            updated += 1
        else:
            by_id[rid] = r
            added += 1

    catalog["recipes"] = list(by_id.values())
    CATALOG.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    print(f"Done. Added: {added}, Updated: {updated}, Total: {len(catalog['recipes'])}")

if __name__ == "__main__":
    main()
