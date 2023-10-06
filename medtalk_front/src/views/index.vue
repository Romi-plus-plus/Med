<template>
  <div>
    <div class="absolute-center custom-caption">
      <div class="text-h2 text-green-2">东南大学天下第一</div>
      <div class="text-h3 text-light-green-2">最好的大学</div>
      <div class="text-h4 text-teal-2">好的大学，没有天花板</div>
      <q-btn color="green" glossy size="lg" label="点击出发" @click="onStart" />
    </div>
  </div>
</template>

<script setup lang="ts">
const $router = useRouter();

const onStart = () => {
  $router.push({ name: "display" });
};
</script>

<style scoped lang="scss">
.custom-caption {
  text-align: center;
  padding: 12px;
  color: white;
  background-color: rgba(0, 0, 0, 0.4);
  width: 100%;

  > * {
    margin: 16px;
  }
}
</style>
