<template>
  <div v-if="recipe" class="recipe">
    <div class="toolbar" role="toolbar" aria-label="Recipe controls">
      <label class="toggle" :aria-pressed="metric ? 'true' : 'false'">
        <span class="label">Metric</span>
        <input type="checkbox" v-model="metric" aria-label="Toggle metric units" />
        <span class="slider" aria-hidden="true"></span>
      </label>
    </div>
    <h1>{{ recipe.title }}</h1>
    <div v-if="recipe.source" class="kv" style="margin:4px 0 8px 0">
      Source: <a :href="recipe.source" target="_blank" rel="noopener noreferrer">{{ recipe.source }}</a>
    </div>
    <div class="kv">Servings: {{ recipe.servings }}</div>
    <div class="kv" style="margin-top:6px">Tags: {{ recipe.theme_tags.join(", ") }}</div>

    <IngredientOverview :ingredients="recipe.ingredients" :metric="metric" />

    <IngredientSections
      v-if="view?.ingredient_sections"
      :sections="view.ingredient_sections"
      :ingredients="recipe.ingredients"
      :metric="metric"
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
import { onMounted, ref, watch } from "vue"

defineProps<{
  recipe: Recipe | null
  view: RecipeView | null
}>()

// Persisted metric toggle (default off).
const metric = ref(false)
const KEY = "ai-recipe-helper:metric"
onMounted(() => {
  try {
    const raw = localStorage.getItem(KEY)
    if (raw === "1") metric.value = true
  } catch {}
})
watch(metric, v => {
  try { localStorage.setItem(KEY, v ? "1" : "0") } catch {}
})
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 8px 10px;
  margin: -2px 0 10px auto; /* tuck closer to title */
  border: 1px solid var(--border);
  border-radius: 12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  width: fit-content;
}


/* Toggle switch */
.toggle {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  user-select: none;
}
.toggle .label { opacity: .85; font-weight: 600; letter-spacing: .2px }
.toggle input {
  position: absolute;
  opacity: 0;
  width: 0; height: 0;
}
.toggle .slider {
  width: 44px; height: 24px; border-radius: 999px;
  background: rgba(148,163,184,0.35);
  border: 1px solid rgba(148,163,184,0.35);
  position: relative;
  transition: background .2s ease, border-color .2s ease;
}
.toggle .slider::after {
  content: "";
  position: absolute; top: 50%; left: 2px;
  width: 18px; height: 18px; border-radius: 50%;
  transform: translate(0, -50%);
  background: #eaf0f7;
  box-shadow: 0 1px 2px rgba(0,0,0,0.25);
  transition: transform .2s ease;
}
.toggle input:checked + .slider {
  background: rgba(96,165,250,0.45);
  border-color: rgba(96,165,250,0.65);
}
.toggle input:checked + .slider::after {
  transform: translate(20px, -50%);
}
</style>
