import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIEWS_PATH = ROOT / "data" / "recipe_views.json"

try:
    from models import ViewsFile
except Exception as e:
    print(f"Unable to import models: {e}")
    sys.exit(1)

try:
    raw = json.loads(VIEWS_PATH.read_text(encoding="utf-8"))
except json.JSONDecodeError as je:
    print("Views JSON: FAIL (invalid JSON)")
    print(f"{je}")
    sys.exit(1)

try:
    ViewsFile.model_validate(raw)
    print("Views validation: PASS")
except Exception as e:
    print("Views validation: FAIL")
    print(e)
    sys.exit(1)
