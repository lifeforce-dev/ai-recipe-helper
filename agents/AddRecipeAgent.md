
# Agent: AddRecipeAgent

## Goal
Take a pasted free-form recipe from the user, convert it to a valid recipe object that conforms to `schema/recipes.schema.json`, and append/update it in `data/recipes.json`.
This json file will be used by another agent to select recipes from the json list that include similar ingredients to cook for the week.

## Rules
- Use `templates/recipe_template.json` as the structural reference.
- Generate a `recipe_id` slug: lowercase, a–z, 0–9, `_` or `-`. Prefer short, descriptive slugs.
- Normalize ingredient names to snake_case (e.g., "Soy Sauce" -> "soy_sauce").
- Choose units from the user's conventions: lb, count, cup, cup_dry, tbsp, tsp, clove, etc.
 - Preserve grams exactly when provided in the source. Do not convert to ounces/cups unless the source used them. Avoid unnecessary unit conversions in general.
 - Set `theme_tags` to something reasonable for each recipe. Prefer existing tags; add new tags only when necessary.
 - Set `category` to one of: meat | produce | dairy | grain_legume | spice_herb | condiment | oil_fat | other (matches schema).
 - Set `storage` to one of: pantry | refrigerated | frozen (matches schema).
 - Keep `instructions` clear; concision is fine only when it does NOT remove sequencing, dependencies, or safety context. If in doubt, preserve the original wording.
 - Validate against `schema/recipes.schema.json`.
 - Merge directly into `data/recipes.json` without external scripts:
   - If `data/recipes.json` does not exist, create it with `{ "recipes": [] }`.
   - If an entry with the same `recipe_id` exists, update it in place; otherwise append.

### Non‑simplification principle
- Always maintain functional identity and ordering of the original recipe. Never compress multiple operational steps into one if it obscures sequence or timing.
- Do not drop critical cues (e.g., heat levels, durations, texture checks) in the name of brevity.

## Input Format (from user)
- Arbitrary text blocks or bullet lists that include ingredients and rough steps.

## Output
- Updated `data/recipes.json` with the new entry.
- Show a diff or a success summary.

## Guardrails
- Do not change unrelated files
- Do not invent exotic units; convert to the standard freedom units when possible
- Prefer whole number counts for whole product. Decimals are fine for sauces and weights
- If the user paste includes multiple recipes, process them one by one

## View generation (grouping) — broccoli/stew playbook
- Goal: keep the canonical recipe simple (flat ingredients + single instructions string), but produce a structured view in `data/recipe_views.json` to show prep/cook groups in the UI, matching the broccoli example.
- Always preserve the original order of operations from the user’s instructions. Never invent steps; don’t reorder.
- If groups are not provided, infer them by scanning the instructions top-to-bottom and clustering ingredients that are added together. Typical clusters:
  - Prepped vegetables/aromatics added at once (e.g., onion + radish + mushrooms).
  - Protein with oil/pepper for searing.
  - Sauce or chili oil bloom step (e.g., chili powder in oil).
  - Broth base (e.g., water + gochujang).
  - Seasoning dump (e.g., soy_sauce, tuna_extract, sugar, garlic).
- Quantities in ingredient_sections must match the base recipe amounts; copy over exact `quantity` and `unit`. If an item is a note (e.g., “black pepper generously” or “ice water”), use `{ label, note }` entries instead of fabricating measurements.
- When groups do exist in the user paste, respect them and don’t re-cluster—only normalize naming/units.
- Instruction sections should be short, named, and segmented in the same order as the original steps (e.g., “Prep”, “Pork & Chili Oil”, “Broth & Season”, “Finish”). Each section’s `steps` are concise, declarative sentences.
  - Be concise but functionally identical: retain explicit sequencing, dependencies, and critical cues. When unsure, prefer near‑verbatim phrasing from the source.
- Duplicate ingredient entries in the base recipe that appear at different times (like shaoxing_wine twice) remain as-is in the base array and should be placed in the appropriate view groups by context.

### View merge rules
- File: `data/recipe_views.json` with shape `{ views: RecipeView[] }` (see `web/src/types.ts`).
- If a view for `recipe_id` exists, update it; else append. Keep aliases simple and optional.
- Do not modify views for other recipes.

### Group naming rules (Sectioned Prep)
- Never include "Group n" in a group title.
- Titles must be concise and descriptive so the user can infer usage at a glance (e.g., "Sauce", "Blanching Water", "For Stir‑Fry", "Aromatics", "Broth Base").
- Prefer action/purpose over container numbering (e.g., avoid "Prep – Bowl 2" unless the original recipe explicitly labels it that way and the label carries meaning).
- Keep consistent style across a recipe (e.g., "Finish – Green Onion", "Veg – Add Later").

### Validation checklist (quick)
- Recipe passes `schema/recipes.schema.json`.
- ingredients use snake_case item names and standard units.
- View ingredient_sections include quantities for real items; labels carry no fabricated numbers.
- Instruction order matches the source; no new steps were invented.
 - Functional identity preserved: no context loss from oversimplification; original sequencing and intent are intact.

## Additional guidance: How to infer prep groupings when there are none provided

Goal: Pre‑batch ingredients so each step is a single dump of one group.

- If groupings already exist, skip this section. They may be named differently in the text (e.g., "prep bowls", "bowls"), but they serve the same purpose.
- Scan the instructions and mark each point an ingredient is added (an "ingredient‑use event").
  - Create a new group for each event; the group’s contents are the ingredients added during that event.

Example:

- Stir‑fry the pork in oil.
- Add mushrooms, radish, and potatoes.
- Add garlic.
- Top with green onion.

In this example there are four groups. The first group contains just pork and oil; the second contains mushrooms, radish, and potato; the third contains garlic; the fourth contains green onion.

Caveat: Pay close attention to the wording. Multiple ingredients in one sentence don’t automatically belong to the same group—grouping must match when they’re actually added.

Example:

- Add the oil and garlic and fry for about 20 seconds, then add the pork and sauce, and stir‑fry for another minute.

In this case, there are two groups. Oil and garlic are in the first group because they’re added together initially. Pork and sauce form a second, later group. If you put pork in the first group, it would be added too early (before the 20‑second fry step).
