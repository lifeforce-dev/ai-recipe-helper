<template>
  <div class="section">
    <h2>Ingredient Overview</h2>
    <div class="rows col">
      <DotRow v-for="(ing, i) in ingredients" :key="i" :item="ing.item" :qty="ing.quantity" :unit="ing.unit" />
    </div>
  </div>
</template>

<script setup lang="ts">
import DotRow from "./DotRow.vue"
import type { Ingredient } from "../types"

defineProps<{ ingredients: Ingredient[] }>()
</script>

<style scoped>
.col { display: flex; flex-direction: column; gap: 6px; }
</style>
