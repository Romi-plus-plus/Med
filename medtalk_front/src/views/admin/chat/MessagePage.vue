<template>
  <admin-page>
    <div class="row" v-if="stats">
      <div class="col-5">
        <admin-section-card>
          <div class="row q-col-gutter-lg">
            <progress-card
              title="😅总数"
              :value="stats.total"
              :progress="1"
              color="brown-14"
              indeterminate
              class="col-5"
            />
            <progress-card
              title="今日😅"
              :progress="stats.total_today / stats.total_yesterday"
              color="brown-14"
              class="col-7"
            >
              <template #value>
                {{ stats.total_today }}
                <span style="font-size: 60%">{{ inc_rate(stats.total_today, stats.total_yesterday) }}</span>
              </template>
            </progress-card>
            <progress-card
              title="👍总数"
              :value="stats.total_like"
              :progress="1"
              color="green-14"
              indeterminate
              class="col-5"
            />
            <progress-card
              title="今日👍"
              :progress="stats.total_like_today / stats.total_like_yesterday"
              color="green-13"
              class="col-7"
            >
              <template #value>
                {{ stats.total_like_today }}
                <span style="font-size: 60%">{{ inc_rate(stats.total_like_today, stats.total_like_yesterday) }}</span>
              </template>
            </progress-card>
            <progress-card
              title="👎总数"
              :value="stats.total_dislike"
              :progress="1"
              color="red-14"
              indeterminate
              class="col-5"
            />
            <progress-card
              title="今日👎"
              :progress="stats.total_dislike_today / stats.total_dislike_yesterday"
              color="red-13"
              class="col-7"
            >
              <template #value>
                {{ stats.total_dislike_today }}
                <span style="font-size: 60%">
                  {{ inc_rate(stats.total_dislike_today, stats.total_dislike_yesterday) }}
                </span>
              </template>
            </progress-card>
          </div>
        </admin-section-card>
      </div>
      <div class="col">
        <admin-section-card>
          <feedback-gauge :data="stats" style="height: 250px" />
        </admin-section-card>
      </div>
    </div>
    <admin-section-card v-if="stats">
      <!-- <q-card-section> -->
      <feedback-chart :data="stats" style="height: 240px" />
      <!-- </q-card-section> -->
    </admin-section-card>
    <admin-section-card>
      <feedback-table />
    </admin-section-card>
  </admin-page>
</template>

<script setup lang="ts">
import { FeedbackStats, getFeedbackStats } from "@/api/feedback";
import FeedbackChart from "./components/FeedbackChart.vue";
import FeedbackGauge from "./components/FeedbackGauge.vue";
import FeedbackTable from "./components/FeedbackTable.vue";

const stats = ref<FeedbackStats>();

onMounted(updateStats);

async function updateStats() {
  stats.value = await getFeedbackStats();
}

function inc_rate(a: number, b: number) {
  return `${a >= b ? "+" : ""}${(((a - b) / b) * 100).toFixed(1)}%`;
}
</script>

<style scoped></style>
