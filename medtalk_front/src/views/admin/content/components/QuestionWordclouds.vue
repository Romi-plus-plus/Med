<template>
  <div class="row">
    <div class="col-4">
      <admin-section-card class="aspect-square">
        <div class="text-h6 text-center">词语</div>
        <q-separator />
        <word-cloud :data="stats.word" :mask-image="imageMask1" />
      </admin-section-card>
    </div>
    <div class="col-4">
      <admin-section-card class="aspect-square">
        <div class="text-h6 text-center">意图</div>
        <q-separator />
        <word-cloud :data="stats.intent" :mask-image="imageMask2" />
      </admin-section-card>
    </div>
    <div class="col-4">
      <admin-section-card class="aspect-square">
        <div class="text-h6 text-center">实体</div>
        <q-separator />
        <word-cloud :data="stats.entity" :mask-image="imageMask3" />
      </admin-section-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { QuestionStats, getQuestionStats } from "@/api/question";
import imageMask1 from "@/assets/img/cloud1.base64?raw";
import imageMask2 from "@/assets/img/cloud3.base64?raw";
import imageMask3 from "@/assets/img/cloud3.base64?raw";

const stats = ref<QuestionStats>({ word: {}, intent: {}, entity: {} });

onMounted(updateStats);

async function updateStats() {
  stats.value = await getQuestionStats();
}
</script>

<style scoped></style>
