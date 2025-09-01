<template>
  <div class="section">
    <h2>Cooking</h2>
    <div class="section-hint">Do these groups in order.</div>

    <!-- Row bands: each band spans two columns to encourage left-to-right flow per row. -->
    <div class="rows-outer">
      <div
        v-for="(row, r) in rows"
        :key="r"
        class="row-band"
        :class="{ even: r % 2 === 0, odd: r % 2 === 1 }"
      >
        <div class="grid-two">
          <div v-for="(sec, j) in row.items" :key="j" class="panel">
            <div class="kv" style="margin-bottom:8px">{{ row.startIndex + j + 1 }}. {{ sec.name }}</div>
            <div class="steps">
              <div v-for="(s, k) in sec.steps" :key="k" class="stepRow">
                <div class="num">{{ k + 1 }}</div>
                <div class="step">{{ s }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup lang="ts">
import type { InstructionSection } from "../types"
import { computed } from "vue"

const props = defineProps<{ sections: InstructionSection[] }>()

// Group instruction sections into visual rows of two.
const rows = computed(() => {
  const out: { startIndex: number; items: InstructionSection[] }[] = []
  for (let i = 0; i < props.sections.length; i += 2) {
    out.push({ startIndex: i, items: props.sections.slice(i, i + 2) })
  }
  return out
})
</script>

<style scoped>
.rows-outer { display: flex; flex-direction: column; gap: 12px }

/* Subtle colored band behind each pair of panels. */
.row-band {
  position: relative;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 10px 10px 10px 14px; /* a bit more left padding for accent rail */
  background: var(--rowband-even-bg);
}
.row-band.even { border-color: var(--rowband-even-border) }
.row-band.odd {
  background: var(--rowband-odd-bg);
  border-color: var(--rowband-odd-border);
}

/* Left accent rail to strengthen row identity. */
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
.steps { display: flex; flex-direction: column; gap: 8px; }
.stepRow { display: flex; align-items: flex-start; gap: 10px; }
.num {
  width: 24px; height: 24px; border-radius: 50%;
  background: var(--step-badge-bg);
  border: 1px solid var(--step-badge-border);
  color: var(--step-badge-text);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 12px; margin-top: 2px;
}
.step { flex: 1; }
</style>
