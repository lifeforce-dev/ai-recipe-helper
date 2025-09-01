<template>
  <div class="section">
    <h2>Sectioned Prep</h2>
    <div class="grid-two">
      <div v-for="(sec, i) in sections" :key="i" class="panel">
        <div class="kv" style="margin-bottom:8px">{{ i + 1 }}. {{ sec.name }}</div>
        <div class="rows col">
          <template v-for="(it, j) in sec.items" :key="j">
            <template v-if="'item' in it">
              <DotRow
                :item="(it as any).item"
                :qty="(it as any).quantity ?? findDefault((it as any).item, (it as any).from_index, (it as any).portion).qty"
                :unit="(it as any).unit ?? findDefault((it as any).item, (it as any).from_index, (it as any).portion).unit"
              />
            </template>
            <DotRow v-else :left="(it as any).label" :right="(it as any).note ?? ''" />
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

const props = defineProps<{ sections: IngredientSection[]; ingredients: Ingredient[] }>()

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
</script>

<style scoped>
.col { display: flex; flex-direction: column; gap: 6px; }
</style>
