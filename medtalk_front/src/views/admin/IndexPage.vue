<template>
  <admin-page>
    <div class="row">
      <question-wordclouds class="col" />
      <admin-section-card v-if="feedbackStats" class="col-3">
        <feedback-gauge :data="feedbackStats" />
      </admin-section-card>
    </div>
    <admin-section-card v-if="chatStats">
      <chat-chart :data="chatStats" style="height: 190px" />
    </admin-section-card>
    <div class="row" style="height: 200px">
      <admin-section-card v-if="feedbackStats" class="col">
        <feedback-chart :data="feedbackStats" />
      </admin-section-card>
      <admin-section-card v-if="complaintStats" class="col">
        <complaint-chart :data="complaintStats" />
      </admin-section-card>
    </div>
  </admin-page>
</template>

<script setup lang="ts">
import { ChatStats, getChatStats } from "@/api/chat";
import { ComplaintStats, getComplaintStats } from "@/api/complaint";
import { FeedbackStats, getFeedbackStats } from "@/api/feedback";
import ChatChart from "./chat/components/ChatChart.vue";
import FeedbackChart from "./chat/components/FeedbackChart.vue";
import FeedbackGauge from "./chat/components/FeedbackGauge.vue";
import QuestionWordclouds from "./content/components/QuestionWordclouds.vue";
import ComplaintChart from "./user/components/ComplaintChart.vue";

const chatStats = ref<ChatStats>();
const feedbackStats = ref<FeedbackStats>();
const complaintStats = ref<ComplaintStats>();

onMounted(async () => {
  chatStats.value = await getChatStats();
  feedbackStats.value = await getFeedbackStats();
  complaintStats.value = await getComplaintStats();
});
</script>
<style scoped></style>
