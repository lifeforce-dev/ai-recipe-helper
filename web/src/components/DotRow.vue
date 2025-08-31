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
  if (props.qty != null && props.unit) return stripZero(props.qty) + " " + props.unit
  return props.right ?? ""
})

function stripZero(n: number) {
  return Number.isInteger(n) ? String(n) : String(n).replace(/\.0+$/, "")
}
</script>
