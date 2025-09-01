<template>
  <div class="row">
    <div class="left">{{ left }}</div>
    <div class="fill" />
    <div class="right">{{ right }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { pretty } from "../data"

const props = defineProps<{ left?: string; right?: string; item?: string; qty?: number; unit?: string }>()

const left = computed(() => (props.item ? pretty(props.item) : props.left ?? ""))
const right = computed(() => {
  if (props.qty != null && props.unit) return formatQty(props.qty) + " " + props.unit
  return props.right ?? ""
})

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
</script>
