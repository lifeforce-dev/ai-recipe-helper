<template>
  <div class="section">
    <div class="section-head">
      <h2>Ingredient Overview</h2>
      <div class="section-hint">All ingredients at a glance.</div>
    </div>
    <div class="rows col">
      <DotRow
        v-for="(ing, i) in ingredients"
        :key="i"
        :item="ing.item"
        :qty="ing.quantity"
        :unit="ing.unit"
        :metric="metric"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import DotRow from "./DotRow.vue"
import type { Ingredient } from "../types"

defineProps<{ ingredients: Ingredient[]; metric?: boolean }>()
</script>

<style scoped>
.col { display: flex; flex-direction: column; gap: 6px; }
/* Section scaffold */
.section-head {
  padding: 10px 12px;
  margin: 0 0 8px 0;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
}
.section-head h2 { margin: 0 0 2px 0; font-size: 18px; letter-spacing: .2px }
.section-head .section-hint { margin: 0; opacity: .75 }
</style>
