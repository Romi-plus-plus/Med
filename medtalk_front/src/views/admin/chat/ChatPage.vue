<template>
  <admin-page>
    <div class="row" v-if="stats">
      <div class="col">
        <admin-section-card>
          <div class="row q-col-gutter-lg">
            <progress-card
              title="会话总数"
              :value="stats.total_chats"
              :progress="1"
              color="pink"
              indeterminate
              class="col-6"
            />
            <progress-card
              title="对话总数"
              :value="stats.total_messages"
              :progress="1"
              color="indigo"
              indeterminate
              class="col-6"
            />
            <progress-card
              title="今日会话"
              :value="stats.total_chats_today"
              :progress="stats.total_chats_today / stats.total_chats_yesterday"
              color="pink-12"
              class="col-6"
            />
            <progress-card
              title="今日对话"
              :value="stats.total_messages_today"
              :progress="stats.total_messages_today / stats.total_messages_yesterday"
              color="indigo-13"
              class="col-6"
            />
            <progress-card title="昨日会话" :value="stats.total_chats_yesterday" color="pink-11" class="col-6" />
            <progress-card title="昨日对话" :value="stats.total_messages_yesterday" color="indigo-12" class="col-6" />
          </div>
        </admin-section-card>
      </div>
      <div class="col-8">
        <admin-section-card>
          <chat-chart :data="stats" style="height: 200px" />
        </admin-section-card>
      </div>
    </div>
    <admin-section-card>
      <chat-table />
    </admin-section-card>
  </admin-page>
</template>

<script setup lang="ts">
import { ChatStats, getChatStats } from "@/api/chat";
import ChatChart from "./components/ChatChart.vue";
import ChatTable from "./components/ChatTable.vue";

const stats = ref<ChatStats>();

onMounted(updateStats);

async function updateStats() {
  stats.value = await getChatStats();
}
</script>

<style scoped></style>
