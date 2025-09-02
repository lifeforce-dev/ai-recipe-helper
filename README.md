DISCLAIMER: Code directed by me, written almost entirely by AI

Live app: http://lifeforce-dev.github.io/ai-recipe-helper/

AI‑Recipe‑Helper
================
Simple workflow to collect recipes, view them in a clean prep UI, and plan shopping lists.

What’s here
-----------
- data/ — your editable source of truth
  - recipes.json     (catalog of recipes)
  - inventory.json   (what you have on hand)
- schema/
  - recipes.schema.json (JSON Schema for validation)
- scripts/
  - merge_recipes.py (append/update a recipe by recipe_id)
  - planner_json.py  (compute overlaps and create a shopping list)
- templates/
  - recipe_template.json (starter for a new recipe)
- agents/
  - AddRecipeAgent.md (instructions for adding recipes via Copilot)
- web/
  - Vite + Vue 3 UI that renders your data; deployable to GitHub Pages

Current UI features
-------------------
- Ingredient Overview with tidy dot leaders.
- Sectioned Prep groups with per‑group quantities and notes.
- Metric toggle (toolbar) — switch between freedom units and metric; grams are rounded to whole grams.

Typical flow
------------
1) Add a recipe using agents/AddRecipeAgent.md (or edit JSON directly using templates/recipe_template.json).
2) Save to data/recipes.json using scripts/merge_recipes.py.
3) (Optional) Generate a plan + shopping list with scripts/planner_json.py.
4) Run the web UI to browse and cook.

Local development (web UI)
--------------------------
Prerequisite: Node.js LTS (https://nodejs.org/)

Run the dev server
```powershell
# From the repo root
cd web
npm ci   # or: npm install
npm run dev
```
Notes
- Dev/build scripts copy data/*.json into web/public/data so the UI can load them.
- Edit JSON in data/ and refresh the browser.

Build a production bundle
```powershell
cd web
npm run build
npm run preview  # serve the built app locally
```

Deploy to GitHub Pages
- A workflow builds and deploys web/dist from the release branch. See web/README-PAGES.md.

Troubleshooting
- “vite: command not found”: ensure Node is installed; restart your terminal.
- Port busy: `npm run dev -- --port 5174`.

Notes
- Keep units consistent between inventory and recipes for correct stock math.
- Don’t hand‑edit files under web/public/data; they are generated from data/.
