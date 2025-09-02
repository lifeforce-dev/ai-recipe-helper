"""
merge_recipes.py
- Merge recipes into data/recipes.json using Pydantic models and a canonical JSON format.

Usage:
    python merge_recipes.py path/to/new_recipes.json [path/to/dest_recipes.json]

Where new_recipes.json can be either:
    {"recipes": [ ... ]}  OR  a single recipe object {...}
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List

from models import RecipeCatalog, Recipe

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CATALOG = DATA / "recipes.json"


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def normalize_incoming(obj) -> List[Recipe]:
    if isinstance(obj, dict) and "recipes" in obj:
        return [Recipe.model_validate(r) for r in obj["recipes"]]
    if isinstance(obj, list):
        return [Recipe.model_validate(r) for r in obj]
    return [Recipe.model_validate(obj)]


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python merge_recipes.py path/to/new_recipes.json [path/to/dest_recipes.json]")
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"Not found: {src}")
        sys.exit(1)
    dest_path = Path(sys.argv[2]) if len(sys.argv) == 3 else CATALOG

    incoming_raw = load_json(src)
    incoming = normalize_incoming(incoming_raw)

    existing = RecipeCatalog.model_validate(load_json(dest_path))
    by_id = {r.recipe_id: r for r in existing.recipes}

    added, updated = 0, 0
    for r in incoming:
        if r.recipe_id in by_id:
            by_id[r.recipe_id] = r
            updated += 1
        else:
            by_id[r.recipe_id] = r
            added += 1

    # Preserve original order; append new ones at the end.
    original_ids = [r.recipe_id for r in existing.recipes]
    merged_list: List[Recipe] = []
    # Keep originals (updated entries swapped in by_id)
    for rid in original_ids:
        merged_list.append(by_id[rid])
    # Append any brand-new ones in incoming order
    for r in incoming:
        if r.recipe_id not in original_ids:
            merged_list.append(r)

    out = RecipeCatalog(recipes=merged_list)
    # Write using json.dumps of model_dump for consistent formatting and Unicode.
    dest_path.write_text(json.dumps(out.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Done. Added: {added}, Updated: {updated}, Total: {len(out.recipes)} -> {dest_path}")


if __name__ == "__main__":
    main()
