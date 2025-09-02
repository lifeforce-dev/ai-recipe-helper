"""
merge_recipe_views.py
- Append one or more recipe views to data/recipe_views.json, modeled by Pydantic.

Usage:
    python merge_recipe_views.py path/to/new_recipe_views.json [path/to/dest_recipe_views.json]

Where new_recipe_views.json can be any of:
    {"views": [ ... ]}
    [ {view...}, {view...} ]
    {view...}
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List

from models import ViewsFile, RecipeView

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DEST = DATA / "recipe_views.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_incoming(obj) -> List[RecipeView]:
    if isinstance(obj, dict) and "views" in obj:
        return [RecipeView.model_validate(v) for v in obj["views"]]
    if isinstance(obj, list):
        return [RecipeView.model_validate(v) for v in obj]
    return [RecipeView.model_validate(obj)]


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python merge_recipe_views.py path/to/new_recipe_views.json [path/to/dest_recipe_views.json]")
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"Not found: {src}")
        sys.exit(1)

    dest_path = Path(sys.argv[2]) if len(sys.argv) == 3 else DEST

    incoming_raw = load_json(src)
    incoming = normalize_incoming(incoming_raw)

    existing = ViewsFile.model_validate(load_json(dest_path))
    by_id = {v.recipe_id: v for v in existing.views}

    added, updated = 0, 0
    for v in incoming:
        if v.recipe_id in by_id:
            by_id[v.recipe_id] = v
            updated += 1
        else:
            by_id[v.recipe_id] = v
            added += 1

    # Preserve original order; append new ones at end.
    original_ids = [v.recipe_id for v in existing.views]
    merged_list: List[RecipeView] = []
    for rid in original_ids:
        merged_list.append(by_id[rid])
    for v in incoming:
        if v.recipe_id not in original_ids:
            merged_list.append(v)

    out = ViewsFile(views=merged_list)
    # Write using json.dumps of model_dump for consistent formatting and Unicode.
    dest_path.write_text(
        json.dumps(out.model_dump(exclude_none=True), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Done. Added: {added}, Updated: {updated}, Total: {len(out.views)} -> {dest_path}")


if __name__ == "__main__":
    main()
