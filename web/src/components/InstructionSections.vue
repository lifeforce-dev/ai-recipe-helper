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
            <div v-for="(s, j) in sec.steps" :key="j" class="stepRow">
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
</script>

<style scoped>
.single-col { max-width: 760px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px }

/* Alternating row backgrounds and accent rail (same scheme as two-column version). */
.row-band {
  position: relative;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px;
  padding: 8px 10px 8px 14px;
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
.num {
  width: 20px; height: 20px; border-radius: 50%;
  background: var(--step-badge-bg);
  border: 1px solid var(--step-badge-border);
  color: var(--step-badge-text);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 11px; margin-top: 2px;
}
.step { flex: 1; }

/* Prominent panel header with index badge; color harmonizes with row theme. */
.panel-title { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; padding: 4px 0 6px; border-bottom: 1px solid rgba(255,255,255,0.06) }
.panel-name { font-weight: 700; font-size: 17px; letter-spacing: .2px }

/* Section scaffold (non-sticky) with a soft badge background. */
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
