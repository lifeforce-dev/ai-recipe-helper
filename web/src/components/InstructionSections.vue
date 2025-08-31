<template>
  <div class="section">
    <h2>Cooking</h2>
    <div class="section-hint">Do these groups in order.</div>
    <div class="grid-two">
      <div v-for="(sec, i) in sections" :key="i" class="panel">
        <div class="kv" style="margin-bottom:8px">{{ i + 1 }}. {{ sec.name }}</div>
        <div class="steps">
          <div v-for="(s, j) in sec.steps" :key="j" class="stepRow">
            <div class="num">{{ j + 1 }}</div>
            <div class="step">• {{ s }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { InstructionSection } from "../types"

defineProps<{ sections: InstructionSection[] }>()
</script>

<style scoped>
.steps { display: flex; flex-direction: column; gap: 8px; }
.stepRow { display: flex; align-items: flex-start; gap: 10px; }
.num {
  width: 24px; height: 24px; border-radius: 50%;
  background: var(--muted-2); color: var(--fg);
  display: flex; align-items: center; justify-content: center;
  font-weight: 600; font-size: 12px; margin-top: 2px;
}
.step { flex: 1; }
</style>
