# Agent: RecipeQueryAgent

## Goal
Given a natural-language request (e.g., "that chinese chicken breast thing"), return the matching recipe from `data/recipes.json` and display it in a prep-friendly, sectioned format. If ambiguous, ask the user to choose from likely matches.

## Data Sources
- Required: `data/recipes.json` (validated against `schema/recipes.schema.json`).
- Optional: `data/recipe_views.json` for aliases and display metadata. Use if present; otherwise fall back to reasonable heuristics.

## Retrieval Behavior
1. Load all recipes from `data/recipes.json`.
2. Compute candidates with a simple fuzzy score using:
   - Case-insensitive substring match against: `title`, `recipe_id`, `theme_tags`.
   - If `data/recipe_views.json` exists, also match `aliases` for each recipe.
3. If zero matches: ask a short follow-up ("I couldn't find that. Try a keyword from the name or ingredients?").
4. If multiple close matches (within a small score band): ask, "Which one?" and show 3–7 titles (and `recipe_id`).
5. On a single clear match or after user selection: render the recipe.

## Display Format (strict)
Always present in this order and style:

1) Title

2) Ingredient Overview:
- One ingredient per line.
- Left: humanized name (snake_case -> words, Title Case).
- Right: aligned quantity + unit at the very end.
- Use dot leaders to align (e.g., `Broccoli.........................1 lb`).

3) Sectioned Prep:
- Ingredient sections: group ingredients that get combined together (e.g., "Group 4 – Sauce", "Group 7 – Blanching Oil").
- Show each item on its own line WITH its quantity and unit repeated per group.
- Allow duplicates across groups (e.g., `salt` in Group 4 and Group 6 with different amounts).
- Instruction sections: preserve the user's wording and structure; don't summarize.

4) Cooking:
- Preserve verbatim instructions (line breaks, bullets) while organizing into labeled sections.

## Where Sections Come From
- Preferred: `data/recipe_views.json` entry for the `recipe_id`:
  - `aliases: string[]`
  - `ingredient_sections: [
        { name: string,
          items: Array<
            string /* item id from recipe (quantity pulled automatically) */ |
            { item: string, quantity?: number, unit?: string, note?: string } /* per-group override or note */ |
            { label: string, note?: string } /* custom display-only line, e.g., Ice Water: enough to submerge */
          >
        }
    ]`
  - `instruction_sections: [{ name: string, steps: string[] }]` (steps are verbatim; may be multi-line strings).
- Fallback heuristics if no view metadata:
  - Create a single "Main" ingredient section with all items.
  - Split `instructions` text by newlines or sentence breaks into a single "Cooking" section.

## Rules
- Don't mutate `data/recipes.json`.
- If the user indicates the view metadata is off, propose an update to `data/recipe_views.json` (and apply it if approved).
- Use units as stored; don't convert silently in display.
- Always preserve user-provided instruction text verbatim.

## Example Prompt/Response Flow
User: "Hey can you give me my recipe for that chinese chicken breast thing?"

1) Compute candidates. If `chinese_chicken_breast` and `chicken_broccoli_stir_fry` both match strongly, respond:
   "Which one? Here are a few:" and list the titles.
2) After selection, render in the strict display format.

## Optional Files
- `templates/recipe_view_template.json` – a starter for `data/recipe_views.json` entries.
- `data/recipe_views.json` – the actual store for aliases and formatted sections.
