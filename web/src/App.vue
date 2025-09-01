<template>
  <div class="container">
    <div class="layout" ref="layoutEl" :class="{ 'mobile-snap': isMobile }">
      <div class="panel" ref="leftPanel">
        <div class="panel-head-section">
          <div class="catalog-head">Recipe Catalog</div>
          <div class="panel-search">
            <div class="search">
              <input
                ref="searchInput"
                placeholder="Search recipes (title or alias)…"
                v-model="query"
              />
            </div>
          </div>
        </div>
        <div class="panel-divider"></div>
        <div class="kv" style="margin-bottom:10px">{{ filtered.length }} recipe{{ filtered.length === 1 ? '' : 's' }}</div>
        <div class="list" ref="primaryList">
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
        <div v-if="suggestions.length" class="list" ref="suggestionsList">
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

      <div class="panel" ref="rightPanel">
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
import { computed, onMounted, onUnmounted, ref, watch, nextTick } from "vue"
import Fuse from "fuse.js"
import { loadCatalogs } from "./data"
import type { DisplayEntry } from "./types"
import RecipeView from "./components/RecipeView.vue"

const entries = ref<DisplayEntry[]>([])
const query = ref("")
const activeId = ref<string | null>(null)
const searchInput = ref<HTMLInputElement | null>(null)
const primaryList = ref<HTMLDivElement | null>(null)
const suggestionsList = ref<HTMLDivElement | null>(null)
const layoutEl = ref<HTMLDivElement | null>(null)
const leftPanel = ref<HTMLDivElement | null>(null)
const rightPanel = ref<HTMLDivElement | null>(null)

onMounted(async () => {
  entries.value = await loadCatalogs()
  const id = location.hash.replace("#/recipe/", "")
  if (id) activeId.value = id
  addEventListener("hashchange", () => {
    const id = location.hash.replace("#/recipe/", "")
    activeId.value = id || null
  })

  // Global "/" to focus the search, unless typing in a text field already.
  const onKey = (e: KeyboardEvent) => {
    if (e.key === "/" && !e.metaKey && !e.ctrlKey && !e.altKey) {
      const target = e.target as HTMLElement | null
      const tag = target?.tagName?.toLowerCase()
      const isTyping = tag === "input" || tag === "textarea" || !!target?.isContentEditable
      if (isTyping) {
        return
      }
      e.preventDefault()
      searchInput.value?.focus()
      // Select current text to allow immediate overwrite.
      searchInput.value?.select()
    }
  }
  window.addEventListener("keydown", onKey)

  // Cleanup on unmount to avoid leaks.
  onUnmounted(() => {
    window.removeEventListener("keydown", onKey)
    window.removeEventListener("resize", onResize)
  })

  // Observe resize to update gradient visibility on lists.
  const onResize = () => {
    updateListScrollStates()
    ensureInitialPanel()
  }
  window.addEventListener("resize", onResize)
  await nextTick()
  updateListScrollStates()
  ensureInitialPanel()
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
  // On mobile, snap to recipe panel on selection.
  if (isMobile) {
    nextTick().then(() => scrollToPanel("right"))
  }
}

function updateListScroll(el: HTMLElement | null): void {
  if (!el) return
  const hasScroll = el.scrollHeight > el.clientHeight + 1
  el.classList.toggle("has-scroll", hasScroll)
}
function updateListScrollStates(): void {
  updateListScroll(primaryList.value)
  updateListScroll(suggestionsList.value)
}

// Recompute after data/filter changes.
watch([filtered, suggestions], async () => {
  await nextTick()
  updateListScrollStates()
})

// Mobile snap UX -----------------------------------------------------------
let mql: MediaQueryList | null = null
const isMobile = ref(false)
function setupMedia() {
  mql = window.matchMedia("(max-width: 820px)")
  const apply = () => (isMobile.value = !!mql && mql.matches)
  apply()
  mql.addEventListener("change", () => {
    apply()
    // When switching breakpoints, make sure the correct panel is in view.
    nextTick().then(() => ensureInitialPanel())
  })
}
setupMedia()

function scrollToPanel(which: "left" | "right") {
  const el = layoutEl.value
  if (!el) return
  const target = which === "left" ? leftPanel.value : rightPanel.value
  if (!target) return
  el.scrollTo({ left: target.offsetLeft, behavior: "smooth" })
}
function ensureInitialPanel() {
  if (!isMobile.value) return
  const hasRecipe = !!activeEntry.value
  scrollToPanel(hasRecipe ? "right" : "left")
}
</script>
