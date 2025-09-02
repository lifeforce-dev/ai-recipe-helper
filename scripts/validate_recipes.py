import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "recipes.schema.json"
RECIPES_PATH = ROOT / "data" / "recipes.json"

try:
    import jsonschema
    from jsonschema import validate
except Exception as e:
    print("jsonschema not available; skipping strict validation.")
    sys.exit(0)

schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
recipes = json.loads(RECIPES_PATH.read_text(encoding="utf-8"))

try:
    validate(instance=recipes, schema=schema)
    print("Schema validation: PASS")
except jsonschema.ValidationError as ve:
    print("Schema validation: FAIL")
    print(ve)
    sys.exit(1)
