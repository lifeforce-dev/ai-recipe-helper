<template>
  <div class="section">
    <h2>Cooking</h2>
    <div class="section-hint">Do these groups in order.</div>

    <!-- Single centered column using original panel/step colors. -->
    <div class="single-col">
      <div
        v-for="(sec, i) in sections"
        :key="i"
        class="row-band"
        :class="{ even: i % 2 === 0, odd: i % 2 === 1 }"
      >
        <div class="panel">
          <div class="panel-title" role="heading" aria-level="3">
            <span class="panel-index">{{ i + 1 }}</span>
            <span class="panel-name">{{ sec.name }}</span>
          </div>
          <div class="steps">
            <div
              v-for="(s, j) in sec.steps"
              :key="j"
              class="stepRow"
              :class="{ selected: isSelected(i, j) }"
              role="button"
              tabindex="0"
              @click="toggleSelected(i, j)"
              @keydown.enter.prevent="toggleSelected(i, j)"
              @keydown.space.prevent="toggleSelected(i, j)"
              :aria-pressed="isSelected(i, j) ? 'true' : 'false'"
            >
              <div class="num">{{ j + 1 }}</div>
              <div class="step">{{ s }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup lang="ts">
import type { InstructionSection } from "../types"

defineProps<{ sections: InstructionSection[] }>()

// Track a single selected step as [section, step].
import { ref } from "vue"
const selected = ref<{ s: number; j: number } | null>(null)
function isSelected(s: number, j: number): boolean {
  return !!selected.value && selected.value.s === s && selected.value.j === j
}
function toggleSelected(s: number, j: number): void {
  if (isSelected(s, j)) {
    selected.value = null
  } else {
    selected.value = { s, j }
  }
}
</script>

<style scoped>
.single-col { max-width: 760px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px }

/* Alternating row backgrounds and accent rail (same scheme as two-column version). */
.row-band {
  position: relative;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 10px 10px 10px 14px;
  background: var(--rowband-even-bg);
}
.row-band.even { border-color: var(--rowband-even-border) }
.row-band.odd { background: var(--rowband-odd-bg); border-color: var(--rowband-odd-border) }
.row-band::before {
  content: "";
  position: absolute;
  left: 6px;
  top: 8px;
  bottom: 8px;
  width: 3px;
  border-radius: 3px;
  background: var(--rowband-even-accent);
  opacity: .9;
}
.row-band.odd::before { background: var(--rowband-odd-accent) }

.steps { display: flex; flex-direction: column; gap: 8px; }
.stepRow { display: flex; align-items: flex-start; gap: 10px; }
.stepRow { cursor: pointer; user-select: none; }
.num {
  width: 24px; height: 24px; border-radius: 50%;
  background: var(--step-badge-bg);
  border: 1px solid var(--step-badge-border);
  color: var(--step-badge-text);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 12px; margin-top: 2px;
}
.step { flex: 1; }

/* Persistent selection state mirrors hover but a bit stronger. */
.stepRow.selected {
  background: rgba(96,165,250,0.12);
  border-color: rgba(96,165,250,0.55);
  box-shadow: inset 0 0 0 1px rgba(96,165,250,0.20);
}

/* Prominent panel header with index badge; color harmonizes with row theme. */
.panel-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 8px 10px;
  box-shadow: inset 0 0 0 1px rgba(0,0,0,0.12);
}
.row-band.even .panel-title { border-color: var(--rowband-even-border); box-shadow: inset 0 0 0 1px rgba(96,165,250,0.12) }
.row-band.odd .panel-title { border-color: var(--rowband-odd-border); box-shadow: inset 0 0 0 1px rgba(52,211,153,0.12) }
.panel-index {
  width: 22px; height: 22px; min-width: 22px; border-radius: 999px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 12px; color: #fff;
  background: var(--rowband-even-accent);
  border: 1px solid rgba(0,0,0,0.35);
}
.row-band.odd .panel-index { background: var(--rowband-odd-accent) }
.panel-name { font-weight: 600; letter-spacing: .2px }
</style>
