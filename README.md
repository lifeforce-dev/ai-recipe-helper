
Recipe Planner Workspace
========================
This folder is ready for VS Code + Copilot (ChatGPT 5) agents.

Structure
---------
data/
  - recipes.json     # your growing catalog (initially empty)
  - inventory.json   # your current stock (edit as you like)
schema/
  - recipes.schema.json
scripts/
  - planner_json.py  # picks overlapping recipes & writes a shopping list
  - merge_recipes.py # safe append/update by recipe_id
templates/
  - recipe_template.json
agents/
  - AddRecipeAgent.md

VS Code niceties
----------------
- .vscode/settings.json binds data/recipes.json -> schema/recipes.schema.json for validation.
- .vscode/tasks.json adds a "Run Meal Planner" task.

Typical flow
------------
1) Paste a messy recipe to your Copilot agent using the instructions in agents/AddRecipeAgent.md.
2) The agent converts it, validates, then runs:
     python scripts/merge_recipes.py <temp.json>
3) Run the planner:
     python scripts/planner_json.py
   Outputs to data/: plan_YYYY-MM-DD.json and shopping_list_YYYY-MM-DD.csv

Notes
-----
- Units must match between inventory and recipe ingredients to subtract stock correctly.
- You can extend the schema with cost, macros, prep time, cuisines, etc.
- If you want automated 4‑day cycles, we can add a scheduler later.
