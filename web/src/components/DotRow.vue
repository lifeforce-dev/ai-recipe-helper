<template>
  <div class="row" ref="rowEl">
    <div class="left" ref="leftEl" :style="leftStyle">{{ left }}</div>
    <div class="fill" ref="fillEl" />
  <div class="right" ref="rightEl" :style="rightStyle">{{ right }}</div>
  </div>
  
</template>

<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, ref, watch, nextTick } from "vue"
import { pretty } from "../data"

const props = defineProps<{
  left?: string
  right?: string
  item?: string
  qty?: number
  unit?: string
  metric?: boolean
  // If true, shrink the left text only when the row runs out of leader space (used by Sectioned groups).
  shrinkLeft?: boolean
  // If true, shrink the right text similarly when space runs out (useful for long notes in sections).
  shrinkRight?: boolean
}>()

const left = computed(() => (props.item ? pretty(props.item) : props.left ?? ""))
const right = computed(() => {
  if (props.qty != null && props.unit) {
    const { qty, unit } = props.metric ? toMetricSmart(props.qty, props.unit, props.item) : { qty: props.qty, unit: props.unit }
    return formatQty(qty) + (unit ? " " + unit : "")
  }
  return props.right ?? ""
})

// --- Adaptive left sizing (section-only) ---
const rowEl = ref<HTMLDivElement>()
const leftEl = ref<HTMLDivElement>()
const rightEl = ref<HTMLDivElement>()
const fillEl = ref<HTMLDivElement>()
const leftFontPx = ref<number | null>(null)
const rightFontPx = ref<number | null>(null)
const leftStyle = computed(() => (props.shrinkLeft && leftFontPx.value ? { fontSize: `${leftFontPx.value}px` } : undefined))
const rightStyle = computed(() => (props.shrinkRight && rightFontPx.value ? { fontSize: `${rightFontPx.value}px` } : undefined))

let ro: ResizeObserver | null = null

async function adjustAdaptiveSize() {
  await nextTick()
  const row = rowEl.value, leftN = leftEl.value, rightN = rightEl.value, fillN = fillEl.value
  if (!row || !leftN || !rightN || !fillN) return

  // Reset any prior sizing to measure natural widths.
  if (props.shrinkLeft) leftFontPx.value = null
  if (props.shrinkRight) rightFontPx.value = null
  await nextTick()

  const baseSize = parseFloat(getComputedStyle(leftN).fontSize || "16") || 16
  const baseSizeRight = parseFloat(getComputedStyle(rightN).fontSize || "16") || 16
  const minFill = 12 // keep at least this many pixels of leader
  const minFontL = Math.max(12, Math.round(baseSize * 0.75)) // don't go below 12px or 75%
  const minFontR = Math.max(12, Math.round(baseSizeRight * 0.75))

  // Measure current layout.
  const containerW = row.clientWidth
  const leftW = leftN.offsetWidth
  const rightW = rightN.offsetWidth
  const fillW = fillN.offsetWidth

  // If we still have enough leader space, do nothing.
  if (fillW >= minFill) return

  // Compute a scale to reclaim at least minFill width.
  const targetLeftMax = containerW - rightW - minFill
  const targetRightMax = containerW - leftW - minFill

  let candidates: Array<{
    side: 'left' | 'right'
    base: number
    minFont: number
    currentW: number
    targetMax: number
  }> = []
  if (props.shrinkLeft) candidates.push({ side: 'left', base: baseSize, minFont: minFontL, currentW: leftW, targetMax: targetLeftMax })
  if (props.shrinkRight) candidates.push({ side: 'right', base: baseSizeRight, minFont: minFontR, currentW: rightW, targetMax: targetRightMax })
  if (candidates.length === 0) return

  // Discard impossible targets.
  candidates = candidates.filter(c => c.targetMax > 0)
  if (candidates.length === 0) {
    // Nothing fits; clamp both sides to minimum if allowed.
    if (props.shrinkLeft) leftFontPx.value = minFontL
    if (props.shrinkRight) rightFontPx.value = minFontR
    return
  }

  // Choose the side that requires the least reduction (largest scale) but still <= 1.
  candidates.sort((a, b) => (b.targetMax / Math.max(1, b.currentW)) - (a.targetMax / Math.max(1, a.currentW)))
  const pick = candidates[0]
  const scale = Math.min(1, pick.targetMax / Math.max(1, pick.currentW))
  let newSize = Math.max(pick.minFont, Math.floor(pick.base * scale))
  if (pick.side === 'left') {
    leftFontPx.value = newSize
  } else {
    rightFontPx.value = newSize
  }
  await nextTick()

  // Safety: if still no leader, clamp the chosen side to its min.
  if (fillN.offsetWidth < minFill) {
    if (pick.side === 'left') leftFontPx.value = pick.minFont
    else rightFontPx.value = pick.minFont
  }
}

onMounted(() => {
  if (props.shrinkLeft || props.shrinkRight) {
    ro = new ResizeObserver(() => adjustAdaptiveSize())
    if (rowEl.value) ro.observe(rowEl.value)
  }
  adjustAdaptiveSize()
})

onBeforeUnmount(() => { if (ro) { ro.disconnect(); ro = null } })

// Recompute when the displayed text changes.
watch([left, right, () => props.shrinkLeft, () => props.shrinkRight], () => adjustAdaptiveSize())

// Render quantities as mixed numbers with nice fraction glyphs where possible.
function formatQty(n: number): string {
  if (!Number.isFinite(n)) return String(n)

  const map: Record<string, string> = {
    "1/2": "½",
    "1/3": "⅓",
    "2/3": "⅔",
    "1/4": "¼",
    "3/4": "¾",
    "1/5": "⅕",
    "2/5": "⅖",
    "3/5": "⅗",
    "4/5": "⅘",
    "1/6": "⅙",
    "5/6": "⅚",
    "1/8": "⅛",
    "3/8": "⅜",
    "5/8": "⅝",
    "7/8": "⅞",
  }

  const sign = n < 0 ? -1 : 1
  let x = Math.abs(n)
  const whole = Math.floor(x + 1e-8)
  let rem = x - whole
  if (rem < 1e-8) return String(sign * whole)

  const dens = [2, 3, 4, 5, 6, 8]
  let bestNum = 0
  let bestDen = 1
  let bestErr = Infinity
  for (const d of dens) {
    const num = Math.round(rem * d)
    const err = Math.abs(rem - num / d)
    if (num === 0) {
      if (err < bestErr) { bestErr = err; bestNum = 0; bestDen = 1 }
      continue
    }
    if (num === d) {
      // Rounds up to a whole.
      return String(sign * (whole + 1))
    }
    if (err < bestErr) { bestErr = err; bestNum = num; bestDen = d }
  }

  // Reduce the fraction to simplest terms.
  const g = gcd(bestNum, bestDen)
  const numR = bestNum / g
  const denR = bestDen / g
  const fracKey = `${numR}/${denR}`
  const frac = map[fracKey] ?? fracKey
  const wholeStr = whole ? String(whole * sign) : (sign < 0 ? "-" : "")
  return whole ? `${wholeStr} ${frac}` : `${wholeStr}${frac}`
}

function gcd(a: number, b: number): number {
  let x = Math.abs(a), y = Math.abs(b)
  while (y) { const t = y; y = x % y; x = t }
  return x || 1
}

// Convert common US cooking units to metric.
function toMetric(qty: number, unit: string): { qty: number; unit: string } {
  const u = unit.toLowerCase()
  // Count-like units stay as-is.
  const countUnits = new Set(["count", "clove", "bunch", "handful", "square"])
  if (countUnits.has(u)) return { qty, unit }

  // Weight
  if (u === "lb" || u === "pound" || u === "lbs") return { qty: round(qty * 453.592, 0), unit: "g" }
  if (u === "oz" || u === "ounce" || u === "ounces") return { qty: round(qty * 28.3495, 0), unit: "g" }

  // Volume
  if (u === "tsp" || u === "teaspoon" || u === "teaspoons") return { qty: round(qty * 5, 0), unit: "ml" }
  if (u === "tbsp" || u === "tablespoon" || u === "tablespoons") return { qty: round(qty * 15, 0), unit: "ml" }
  if (u === "cup" || u === "cups") return { qty: round(qty * 236.588, 0), unit: "ml" }

  // Canned goods by oz -> g (approx weight). Already handled by oz path above.

  // Unknown unit: leave as-is.
  return { qty, unit }
}

// Smart conversion using unit_type on the ingredient when available.
function toMetricSmart(qty: number, unit: string, item?: string): { qty: number; unit: string } {
  // Try to detect unit_type from the displayed item by peeking into a global runtime map, if available.
  // Fallback to simple toMetric if no metadata is available.
  const anyWin = window as any
  const metaMap: Map<string, { unit_type?: string }> | undefined = anyWin.__ING_META__
  const unitType = item && metaMap ? metaMap.get(item)?.unit_type : undefined

  if (unitType === "count") return { qty, unit }
  if (unitType === "mass") {
    // Convert lb/oz to g; if already grams, return as-is; otherwise leave unmodified (unknown mass unit)
    const u = unit.toLowerCase()
    // Item-specific density overrides for spoon/cup measures (grams per teaspoon).
    // Sources: USDA FoodData Central where available. cornstarch: 1 cup = 128 g => 48 tsp => 2.667 g/tsp.
    const gramsPerTsp: Record<string, number> = {
      cornstarch: 128 / 48,
    }
    if (item && gramsPerTsp[item]) {
      const gpt = gramsPerTsp[item]
      if (u === "tsp" || u === "teaspoon" || u === "teaspoons") return { qty: round(qty * gpt, 0), unit: "g" }
      if (u === "tbsp" || u === "tablespoon" || u === "tablespoons") return { qty: round(qty * gpt * 3, 0), unit: "g" }
      if (u === "cup" || u === "cups") return { qty: round(qty * gpt * 48, 0), unit: "g" }
    }
  // Spoon-based measures for mass (approximate densities):
  // Use water-like approximations for simplicity and consistency across powders.
  if (u === "tsp" || u === "teaspoon" || u === "teaspoons") return { qty: round(qty * 5, 0), unit: "g" }
  if (u === "tbsp" || u === "tablespoon" || u === "tablespoons") return { qty: round(qty * 15, 0), unit: "g" }
  if (u === "cup" || u === "cups") return { qty: round(qty * 236.588, 0), unit: "g" }
    if (u === "lb" || u === "pound" || u === "lbs") return { qty: round(qty * 453.592, 0), unit: "g" }
    if (u === "oz" || u === "ounce" || u === "ounces") return { qty: round(qty * 28.3495, 0), unit: "g" }
    if (u === "g" || u === "gram" || u === "grams") return { qty, unit: "g" }
    if (u === "kg" || u === "kilogram" || u === "kilograms") return { qty: round(qty * 1000, 0), unit: "g" }
    return { qty, unit }
  }
  if (unitType === "volume") {
    const u = unit.toLowerCase()
    if (u === "tsp" || u === "teaspoon" || u === "teaspoons") return { qty: round(qty * 5, 0), unit: "ml" }
    if (u === "tbsp" || u === "tablespoon" || u === "tablespoons") return { qty: round(qty * 15, 0), unit: "ml" }
    if (u === "cup" || u === "cups") return { qty: round(qty * 236.588, 0), unit: "ml" }
    if (u === "ml" || u === "milliliter" || u === "milliliters") return { qty, unit: "ml" }
    if (u === "l" || u === "liter" || u === "liters") return { qty: round(qty * 1000, 0), unit: "ml" }
    return { qty, unit }
  }
  // Unknown: fallback to existing heuristic
  return toMetric(qty, unit)
}

function round(n: number, decimals: number): number {
  const f = 10 ** decimals
  return Math.round(n * f) / f
}
</script>
