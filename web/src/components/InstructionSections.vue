<template>
  <div class="section">
    <div class="section-head">
      <h2>Cooking</h2>
      <div class="section-hint">Do these groups in order.</div>
    </div>

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

const props = defineProps<{ sections: InstructionSection[] }>()

// Track a single selected step as [section, step].
import { ref, watch } from "vue"
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

// Bugfix: when the recipe/sections change, clear any prior selection.
watch(
  () => props.sections,
  () => { selected.value = null },
  { deep: false }
)
</script>

<style scoped>
.single-col { max-width: 760px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px }

/* Section header treatment to match Sectioned Prep. */
.section-head {
  padding: 10px 12px;
  margin: 0 0 8px 0;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
}
.section-head h2 { margin: 0 0 2px 0; font-size: 18px; letter-spacing: .2px }
.section-head .section-hint { margin: 0; opacity: .75 }

/* Alternating row backgrounds and accent rail (same scheme as two-column version). */
.row-band {
  position: relative;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px 12px 12px 18px;
  background: var(--rowband-even-bg);
}
.row-band.even { border-color: var(--rowband-even-border) }
.row-band.odd { background: var(--rowband-odd-bg); border-color: var(--rowband-odd-border) }
.row-band::before {
  content: "";
  position: absolute;
  left: 6px;
  top: 10px;
  bottom: 10px;
  width: 2px;
  border-radius: 3px;
  background: var(--rowband-even-accent);
  opacity: .45;
}
.row-band.odd::before { background: var(--rowband-odd-accent) }

.steps { display: flex; flex-direction: column; gap: 8px }
.stepRow { display: flex; align-items: flex-start; gap: 14px }
.stepRow { cursor: pointer; user-select: none; }
.num {
  /* Demoted sub-step number: subdued steel-blue with soft outline. */
  width: 20px; height: 20px; min-width: 20px; border-radius: 50%;
  background: rgba(96, 120, 156, 0.75); /* muted steel-blue @ 75% */
  border: 1px solid rgba(30, 41, 59, 0.45); /* ~45% outline */
  color: #f8fafc;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 11px; margin-top: 2px;
}
.step { flex: 1; line-height: 1.4; font-size: 16px; color: #f1f5f9 }

/* Persistent selection state mirrors hover but a bit stronger. */
/* Local hover: tone down saturation vs. global rule to keep text as star. */
.steps .stepRow:not(.selected):hover {
  background: rgba(255,255,255,0.04);
  border-color: rgba(148,163,184,0.30);
  box-shadow: inset 0 0 0 1px rgba(148,163,184,0.10);
}

/* Selected: vibrant wayfinder state (brighter than hover). */
.stepRow.selected {
  background: rgba(96,165,250,0.12);
  border-color: rgba(96,165,250,0.55);
  box-shadow: inset 0 0 0 1px rgba(96,165,250,0.20);
}
/* Ensure selected always wins, even when hovered (overrides global hover styles). */
.steps .stepRow.selected:hover {
  background: rgba(96,165,250,0.12);
  border-color: rgba(96,165,250,0.55);
  box-shadow: inset 0 0 0 1px rgba(96,165,250,0.20);
}
/* When selected, the number earns the accent so the text still leads at rest. */
.stepRow.selected .num {
  background: var(--step-badge-bg);
  border-color: var(--step-badge-border);
  color: #fff;
}

/* Prominent panel header with index badge; color harmonizes with row theme. */
.panel-title {
  /* Macro anchor: clean text row with divider; not a card. */
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 8px 0 10px 0; /* +top/bottom rhythm */
  margin: 0 0 10px 0;
  border-bottom: 1px solid rgba(148, 163, 184, 0.22);
}
.row-band.even .panel-title { border-color: var(--rowband-even-border) }
.row-band.odd .panel-title { border-color: var(--rowband-odd-border) }
.panel-name {
  /* Clear, prominent section anchor. */
  position: relative;
  font-weight: 700;
  letter-spacing: .2px;
  font-size: 18px; /* + compared to step text */
  color: #eaf0f7;
}
/* Wayfinder underline keyed to the row accent for quick scanning. */
.row-band.even .panel-name::after,
.row-band.odd .panel-name::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -6px;
  height: 3px;
  width: 100%;
  border-radius: 3px;
}
.row-band.even .panel-name::after { background: var(--rowband-even-accent) }
.row-band.odd .panel-name::after { background: var(--rowband-odd-accent) }
</style>
