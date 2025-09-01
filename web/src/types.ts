export type Ingredient = {
	item: string
	quantity: number
	unit: string
	category: string
	storage: string
}
export type Recipe = {
	recipe_id: string
	title: string
	servings: number
	theme_tags: string[]
	ingredients: Ingredient[]
	source?: string
	instructions: string
}
export type RecipeCatalog = { recipes: Recipe[] }

export type ViewItem =
	| { item: string; quantity?: number; unit?: string; note?: string; from_index?: number; portion?: number }
	| { label: string; note?: string }

export type IngredientSection = {
	name: string
	items: ViewItem[]
	rank?: number
}
export type InstructionSection = { name: string; steps: string[] }
export type RecipeView = {
	recipe_id: string
	aliases?: string[]
	ingredient_sections: IngredientSection[]
	instruction_sections: InstructionSection[]
}
export type ViewsCatalog = { views: RecipeView[] }

export type DisplayEntry = {
	recipe: Recipe
	view?: RecipeView
}
