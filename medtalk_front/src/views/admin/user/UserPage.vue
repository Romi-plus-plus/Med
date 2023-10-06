<template>
  <admin-page>
    <admin-section-card v-if="stats">
      <q-card-section>
        <div class="row q-col-gutter-lg">
          <progress-card
            title="总用户数"
            caption="系统总用户数"
            :value="stats.total"
            :progress="1"
            indeterminate
            class="col-3"
          />
          <progress-card
            title="今日注册"
            caption="今日新注册用户数"
            :value="stats.register_today"
            :progress="1"
            color="green"
            class="col-3"
          />
          <progress-card
            title="今日登录"
            caption="今日登录系统用户数"
            :value="stats.login_today"
            :progress="stats.login_today / stats.total"
            color="orange"
            class="col-3"
          />
          <progress-card
            title="今日活跃"
            caption="今日参与聊天用户数"
            :value="stats.active_today"
            :progress="stats.active_today / stats.login_today"
            color="purple"
            class="col-3"
          />
        </div>
      </q-card-section>
    </admin-section-card>
    <admin-section-card>
      <user-table />
    </admin-section-card>
  </admin-page>
</template>

<script setup lang="ts">
import { UserStats, getUserStats } from "@/api/user";
import UserTable from "./components/UserTable.vue";

const stats = ref<UserStats>();

onMounted(updateStats);

async function updateStats() {
  stats.value = await getUserStats();
}
</script>

<style scoped></style>
