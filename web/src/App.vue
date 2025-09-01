<template>
  <div class="container">
    <div class="header">
      <div class="brand">Recipe Catalog</div>
    </div>

    <div class="layout">
      <div class="panel">
        <div class="panel-search">
          <div class="search">
            <input
              placeholder="Search recipes (title or alias)…"
              v-model="query"
            />
          </div>
        </div>
        <div class="kv" style="margin-bottom:10px">{{ filtered.length }} recipe{{ filtered.length === 1 ? '' : 's' }}</div>
        <div class="list">
          <div
            v-for="entry in filtered"
            :key="entry.recipe.recipe_id"
            class="card"
            :class="{ active: entry.recipe.recipe_id === activeId }"
            @click="openRecipe(entry.recipe.recipe_id)"
          >
            <div style="font-weight:600">{{ entry.recipe.title }}</div>
            <div class="badges">
              <span v-for="tag in entry.recipe.theme_tags" :key="tag" class="badge">{{ tag }}</span>
            </div>
          </div>
        </div>

  <div v-if="suggestions.length" class="suggestions-title">Suggestions</div>
  <div v-if="suggestions.length" class="panel-divider"></div>
  <div v-if="suggestions.length" class="kv" style="margin-bottom:10px">{{ suggestions.length }} recipe{{ suggestions.length === 1 ? '' : 's' }}</div>
        <div v-if="suggestions.length" class="list">
          <div
            v-for="entry in suggestions"
            :key="entry.recipe.recipe_id + '-sugg'"
            class="card"
            :class="{ active: entry.recipe.recipe_id === activeId }"
            @click="openRecipe(entry.recipe.recipe_id)"
          >
            <div style="font-weight:600">{{ entry.recipe.title }}</div>
            <div class="badges">
              <span v-for="tag in entry.recipe.theme_tags" :key="tag + '-sugg'" class="badge">{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="panel">
        <RecipeView
          v-if="activeEntry"
          :recipe="activeEntry.recipe"
          :view="activeEntry.view ?? null"
        />
        <div v-else class="kv">Select a recipe to view.</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import Fuse from "fuse.js"
import { loadCatalogs } from "./data"
import type { DisplayEntry } from "./types"
import RecipeView from "./components/RecipeView.vue"

const entries = ref<DisplayEntry[]>([])
const query = ref("")
const activeId = ref<string | null>(null)

onMounted(async () => {
  entries.value = await loadCatalogs()
  const id = location.hash.replace("#/recipe/", "")
  if (id) activeId.value = id
  addEventListener("hashchange", () => {
    const id = location.hash.replace("#/recipe/", "")
    activeId.value = id || null
  })
})

const fuse = computed(() =>
  new Fuse(
    entries.value.map((e: DisplayEntry) => ({ id: e.recipe.recipe_id, title: e.recipe.title, aliases: e.view?.aliases ?? [] })),
    { keys: ["title", "aliases"], threshold: 0.35, ignoreLocation: true }
  )
)

// Secondary index: tags and ingredient item names for suggestions.
const fuseExtras = computed(() =>
  new Fuse(
    entries.value.map((e: DisplayEntry) => ({
      id: e.recipe.recipe_id,
      tags: e.recipe.theme_tags,
      ingredients: e.recipe.ingredients.map(i => i.item)
    })),
    { keys: ["tags", "ingredients"], threshold: 0.3, ignoreLocation: true }
  )
)

const filtered = computed<DisplayEntry[]>(() => {
  if (!query.value.trim()) return entries.value
  const ids = new Set<string>(fuse.value.search(query.value).map((r: any) => (r.item as { id: string }).id))
  return entries.value.filter((e: DisplayEntry) => ids.has(e.recipe.recipe_id))
})

const suggestions = computed<DisplayEntry[]>(() => {
  if (!query.value.trim()) return []
  const primaryIds = new Set<string>(fuse.value.search(query.value).map((r: any) => (r.item as { id: string }).id))
  const extraIds = new Set<string>(fuseExtras.value.search(query.value).map((r: any) => (r.item as { id: string }).id))
  return entries.value.filter(
    (e: DisplayEntry) => extraIds.has(e.recipe.recipe_id) && !primaryIds.has(e.recipe.recipe_id)
  )
})
const activeEntry = computed<DisplayEntry | null>(() =>
  entries.value.find((e: DisplayEntry) => e.recipe.recipe_id === activeId.value) ?? filtered.value[0] ?? null
)

function openRecipe(id: string) {
  location.hash = `#/recipe/${id}`
  activeId.value = id
}
</script>
