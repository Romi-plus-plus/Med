<template>
  <q-dialog v-model="visible" persistent>
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6" style="display: flex; align-items: center">
          <span style="flex: 1">您的笔记</span>
        </div>
      </q-card-section>

      <q-card-section>
        <q-list bordered separator v-if="notes">
          <q-item v-for="msg in notes" :key="msg.id" >
            <q-item-section>{{ msg.content }}</q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="取消" v-close-popup />
        <q-btn flat label="确认" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ChatMessage } from "@/api/chat";

const visible = ref(false);

const props = defineProps<{ notes?: ChatMessage[] }>();

function show() { visible.value = true; }

defineExpose({ show });
</script>

<style scoped></style>
