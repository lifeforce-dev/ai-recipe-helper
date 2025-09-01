import type { RecipeCatalog, ViewsCatalog, DisplayEntry, Recipe, RecipeView } from "./types"

export async function loadCatalogs(): Promise<DisplayEntry[]> {
	const base = (import.meta as any).env?.BASE_URL ?? "/"
	const [rc, vc]: [RecipeCatalog, ViewsCatalog] = await Promise.all([
		fetch(`${base}data/recipes.json`).then(r => r.json()),
		fetch(`${base}data/recipe_views.json`).then(r => r.json())
	])
	const views = new Map<string, RecipeView>(vc.views.map((v: RecipeView) => [v.recipe_id, v]))
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
