<template>
  <q-list bordered separator>
    <q-item-label header>推荐话题</q-item-label>
    <q-separator />
    <q-item v-for="recommend in recommends" :key="recommend.id" clickable @click="sendRecommend(recommend.title)">
      <q-item-section avatar>
        <q-btn flat round icon="whatshot" color="red" />
      </q-item-section>

      <q-item-section class="label-section">
        <q-item-label>{{ recommend.title }}</q-item-label>
        <q-item-label
          caption
          lines="2"
          style="width: 50px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap"
        >
          {{ recommend.content }}
        </q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-item-label caption>{{ formatDateToDay(recommend.add_time) }}</q-item-label>
      </q-item-section>
    </q-item>
    <!-- <chat-input-dialog ref="chatInputRef" /> -->
  </q-list>
</template>

<script setup lang="ts">
import { getRecommendations, Recommendation } from "@/api/recommend";
import { formatDateToDay } from "@/utils/date-utils";

const recommends = ref<Recommendation[]>([]);

// const props = defineProps<{}>();

const emit = defineEmits<{ send: [string] }>();

onMounted(async () => {
  recommends.value = await getRecommendations();
});

function sendRecommend(title: string) {
  emit("send", title);
}
</script>

<style scoped></style>
