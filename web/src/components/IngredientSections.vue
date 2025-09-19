<template>
  <div class="section">
    <div class="section-head">
      <h2>Sectioned Prep</h2>
      <div class="section-hint">Prep by groups so you can cook faster.</div>
    </div>
    <div class="grid-two">
      <div v-for="(sec, i) in sortedSections" :key="i" class="panel">
        <div class="panel-title">
          <span class="panel-name">{{ sec.name }}</span>
        </div>
  <div class="rows col">
          <template v-for="(it, j) in sec.items" :key="j">
            <!-- If item is a non-null string, render as a recipe-linked row; otherwise treat as a label row. -->
            <template v-if="(it as any).item != null">
              <DotRow
                :item="(it as any).item"
                :qty="(it as any).quantity ?? findDefault((it as any).item, (it as any).from_index, (it as any).portion).qty"
    :unit="(it as any).unit ?? findDefault((it as any).item, (it as any).from_index, (it as any).portion).unit"
  :metric="metric"
  :shrink-left="true"
              />
            </template>
            <!-- Label rows can optionally include qty/unit; if absent, fall back to note on the right. -->
            <DotRow
              v-else
              :left="(it as any).label"
              :item="(it as any).item"
              :qty="(it as any).quantity"
              :unit="(it as any).unit"
              :right="(it as any).note ?? ''"
              :metric="metric"
              :shrink-right="true"
            />
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import DotRow from "./DotRow.vue"
import type { IngredientSection, Ingredient } from "../types"
import { computed } from "vue"

const props = defineProps<{ sections: IngredientSection[]; ingredients: Ingredient[]; metric?: boolean }>()

// Build a quick lookup: item -> array of matching recipe ingredients
const byItem = computed(() => {
  const map = new Map<string, Ingredient[]>()
  for (const ing of props.ingredients) {
    const arr = map.get(ing.item) ?? []
    arr.push(ing)
    map.set(ing.item, arr)
  }
  return map
})

function findDefault(item?: string, fromIndex?: number, portion?: number): { qty?: number; unit?: string } {
  if (!item) return {}
  const arr = byItem.value.get(item)
  if (!arr || arr.length === 0) return {}
  let picked: Ingredient | undefined
  if (fromIndex != null) {
    picked = arr[fromIndex]
  } else if (arr.length === 1) {
    picked = arr[0]
  }
  if (!picked) return {}
  const factor = portion != null && portion > 0 ? portion : 1
  return { qty: picked.quantity != null ? picked.quantity * factor : undefined, unit: picked.unit }
}
const sortedSections = computed(() => {
  return [...props.sections].sort((a, b) => (a.rank ?? Infinity) - (b.rank ?? Infinity))
})
</script>

<style scoped>
.col { display: flex; flex-direction: column; gap: 6px; }
/* Reuse header styles from InstructionSections (scoped copy). */
.section-head {
  padding: 10px 12px;
  margin: 0 0 8px 0;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
}
.section-head h2 { margin: 0 0 2px 0; font-size: 18px; letter-spacing: .2px }
.section-head .section-hint { margin: 0; opacity: .75 }

.panel-title { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; padding: 4px 0 6px; border-bottom: 1px solid rgba(255,255,255,0.06) }
.panel-name { font-weight: 700; letter-spacing: .2px }
/* keep previous layout; no forced wrapping */
</style>
