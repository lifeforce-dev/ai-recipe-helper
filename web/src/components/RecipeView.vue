<template>
  <div v-if="recipe" class="recipe">
    <h1>{{ recipe.title }}</h1>
    <div v-if="recipe.source" class="kv" style="margin:4px 0 8px 0">
      Source: <a :href="recipe.source" target="_blank" rel="noopener noreferrer">{{ recipe.source }}</a>
    </div>
    <div class="kv">Servings: {{ recipe.servings }}</div>
    <div class="kv" style="margin-top:6px">Tags: {{ recipe.theme_tags.join(", ") }}</div>

    <IngredientOverview :ingredients="recipe.ingredients" />

    <IngredientSections
      v-if="view?.ingredient_sections"
      :sections="view.ingredient_sections"
      :ingredients="recipe.ingredients"
    />
    <InstructionSections v-if="view?.instruction_sections" :sections="view.instruction_sections" />
  </div>
  <div v-else class="kv">Select a recipe to view details.</div>
</template>

<script setup lang="ts">
import type { Recipe, RecipeView } from "../types"
import IngredientOverview from "./IngredientOverview.vue"
import IngredientSections from "./IngredientSections.vue"
import InstructionSections from "./InstructionSections.vue"

defineProps<{
  recipe: Recipe | null
  view: RecipeView | null
}>()
</script>
