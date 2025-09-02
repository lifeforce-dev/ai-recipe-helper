import type { RecipeCatalog, ViewsCatalog, DisplayEntry, Recipe, RecipeView } from "./types"

export async function loadCatalogs(): Promise<DisplayEntry[]> {
	const base = (import.meta as any).env?.BASE_URL ?? "/"
	const [rc, vc]: [RecipeCatalog, ViewsCatalog] = await Promise.all([
		fetch(`${base}data/recipes.json`).then(r => r.json()),
			fetch(`${base}data/recipe_views.json`).then(r => r.json())
	])
	const views = new Map<string, RecipeView>(vc.views.map((v: RecipeView) => [v.recipe_id, v]))

		// Build a quick global map for unit_type lookup in components (avoids prop drilling everywhere).
		const meta = new Map<string, { unit_type?: string }>()
		for (const rec of rc.recipes) {
			for (const ing of rec.ingredients) {
				if (!meta.has(ing.item)) meta.set(ing.item, { unit_type: (ing as any).unit_type })
			}
		}
		;(window as any).__ING_META__ = meta

	// Use the views as defined in data. Any manual ranks should already be present there.
	return rc.recipes
		.map((recipe: Recipe) => ({ recipe, view: views.get(recipe.recipe_id) }))
		.sort((a: DisplayEntry, b: DisplayEntry) => a.recipe.title.localeCompare(b.recipe.title))
}

export function pretty(label: string): string {
	return label
		.split("_")
		.map(w => w.charAt(0).toUpperCase() + w.slice(1))
		.join(" ")
}
