<template>
  <span class="cursor-pointer" title="点击查看详情" @click="onClick">{{ elliptical }}</span>
</template>

<script setup lang="ts">
const props = defineProps<{ text: string; limit?: int; title?: string; ellipsis?: string }>();

const elliptical = computed(() =>
  !props.limit || props.text.length <= props.limit
    ? props.text
    : props.text.slice(0, props.limit) + (props.ellipsis ?? "……")
);

const $q = useQuasar();

function onClick() {
  $q.dialog({ title: props.title ?? "详情", message: props.text });
}
</script>

<style scoped></style>
