import type { RecipeCatalog, ViewsCatalog, DisplayEntry, Recipe, RecipeView, Ingredient } from "./types"

export async function loadCatalogs(): Promise<DisplayEntry[]> {
	const base = (import.meta as any).env?.BASE_URL ?? "/"
	const [rc, vc]: [RecipeCatalog, ViewsCatalog] = await Promise.all([
		fetch(`${base}data/recipes.json`).then(r => r.json()),
			fetch(`${base}data/recipe_views.json`).then(r => r.json())
	])
	const views = new Map<string, RecipeView>(vc.views.map((v: RecipeView) => [v.recipe_id, v]))

		// Build a quick global map for unit_type lookup in components (avoids prop drilling everywhere).
		// Build a per-item list of explicit metric overrides keyed by the exact base quantity+unit.
		type MetaEntry = { unit_type?: string; quantity?: number; unit?: string; metric_quantity?: number; metric_unit?: string; metric_unit_type?: string }
		const meta = new Map<string, MetaEntry[]>()
		const pushMeta = (ing: Ingredient) => {
			const list = meta.get(ing.item) ?? []
			const entry: MetaEntry = {
				unit_type: (ing as any).unit_type,
				quantity: (ing as any).quantity,
				unit: (ing as any).unit,
				metric_quantity: (ing as any).metric_quantity,
				metric_unit: (ing as any).metric_unit,
				metric_unit_type: (ing as any).metric_unit_type,
			}
			// Only add if it has an explicit metric override.
			if (entry.metric_quantity != null && entry.metric_unit) {
				list.push(entry)
				meta.set(ing.item, list)
			}
		}
		for (const rec of rc.recipes) {
			for (const ing of rec.ingredients) pushMeta(ing)
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
