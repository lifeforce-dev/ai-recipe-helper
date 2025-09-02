from __future__ import annotations

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# ===== Recipes =====

class Ingredient(BaseModel):
	item: str
	quantity: float
	unit: str
	category: Literal[
		"meat",
		"produce",
		"dairy",
		"grain_legume",
		"spice_herb",
		"condiment",
		"oil_fat",
		"other",
	]
	storage: Literal["pantry", "refrigerated", "frozen"]


class Recipe(BaseModel):
	recipe_id: str = Field(pattern=r"^[a-z0-9_\-]+$")
	title: str
	servings: int
	theme_tags: List[str]
	ingredients: List[Ingredient]
	source: Optional[str] = None
	instructions: Optional[str] = None


class RecipeCatalog(BaseModel):
	recipes: List[Recipe]


# ===== Recipe Views =====

class ViewItem(BaseModel):
	item: Optional[str] = None
	label: Optional[str] = None
	quantity: Optional[float] = None
	unit: Optional[str] = None
	note: Optional[str] = None
	from_index: Optional[int] = None


class IngredientSection(BaseModel):
	name: str
	rank: Optional[int] = None
	items: List[ViewItem]


class InstructionSection(BaseModel):
	name: str
	steps: List[str]


class RecipeView(BaseModel):
	recipe_id: str
	aliases: Optional[List[str]] = None
	ingredient_sections: List[IngredientSection]
	instruction_sections: List[InstructionSection]


class ViewsFile(BaseModel):
	views: List[RecipeView]
