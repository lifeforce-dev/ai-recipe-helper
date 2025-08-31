
# Agent: AddRecipeAgent

## Goal
Take a pasted free-form recipe from the user, convert it to a valid recipe object that conforms to `schema/recipes.schema.json`, and append/update it in `data/recipes.json`.

## Rules
- Use `templates/recipe_template.json` as the structural reference.
- Generate a `recipe_id` slug: lowercase, a–z, 0–9, `_` or `-`. Prefer short, descriptive slugs.
- Normalize ingredient names to snake_case (e.g., "Soy Sauce" -> "soy_sauce").
- Choose units from the user's conventions: lb, count, cup, cup_dry, tbsp, tsp, clove, etc.
- Set `category` to one of: meat | produce | dairy | grain_legume | spice_herb | condiment | oil_fat | other, or define your own as needed.
- If you define a new category, make sure to add it to the schema.
- Set `Storage` to one of: pantry | refrigerated | frozen, or define your own as needed.
- If you define a new storage, make sure you add it to the schema.
- Keep `instructions` concise; omit fluff.
- Validate against `schema/recipes.schema.json` (use built-in JSON validation or `jsonschema` if available).

## Input Format (from user)
- Arbitrary text blocks or bullet lists that include ingredients and rough steps.

## Output
- Updated `data/recipes.json` with the new entry.
- Show a diff or a success summary.
