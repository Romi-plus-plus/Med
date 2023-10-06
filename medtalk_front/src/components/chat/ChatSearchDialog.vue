<template>
  <q-dialog v-model="visible" persistent>
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">搜索您的对话</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-input outlined v-model="searchDetail.content" filled @keyup.enter="visible = false" />
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="取消" v-close-popup />
        <q-btn flat label="确认" v-close-popup @click="search" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
// const props = defineProps<{ session: ChatSession }>();

const visible = ref(false);

const searchDetail = ref({
  content: "",
});

function search() {}

function show() {
  visible.value = true;
}

defineExpose({ show });
</script>

<style scoped></style>
