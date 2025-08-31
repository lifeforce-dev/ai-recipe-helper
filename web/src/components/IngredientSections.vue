<template>
  <div class="section">
    <h2>Sectioned Prep</h2>
    <div class="grid-two">
      <div v-for="(sec, i) in sections" :key="i" class="panel">
        <div class="kv" style="margin-bottom:8px">{{ i + 1 }}. {{ sec.name }}</div>
        <div class="rows col">
          <template v-for="(it, j) in sec.items" :key="j">
            <DotRow v-if="'item' in it" :item="(it as any).item" :qty="(it as any).quantity" :unit="(it as any).unit" />
            <DotRow v-else :left="(it as any).label" :right="(it as any).note ?? ''" />
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import DotRow from "./DotRow.vue"
import type { IngredientSection } from "../types"

defineProps<{ sections: IngredientSection[] }>()
</script>

<style scoped>
.col { display: flex; flex-direction: column; gap: 6px; }
</style>
