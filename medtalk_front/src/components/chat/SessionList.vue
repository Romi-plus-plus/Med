<template>
  <div class="sidebar">
    <q-banner rounded :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'" class="h-42">
      <template v-slot:avatar>
        <img src="/img/hospital-logo.webp" style="height: 50px" />
      </template>
    </q-banner>
    <q-list bordered separator>
      <q-item
        v-for="session in sessions"
        :key="session.id"
        :class="{ 'q-item-selected': selectedId === session.id }"
        clickable
        v-ripple
        @click="selectSession(session.id)"
      >
        <q-item-section avatar>
          <q-avatar color="primary-5" text-color="white" rounded class="small-avatar">
            <q-icon :name="isUserMe(session.user_id) ? 'headset_mic' : 'earbuds'" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label v-if="session.title">{{ session.title }}</q-item-label>
          <q-item-label v-else>新的聊天</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-btn flat round push icon="delete" size="sm" class="q-ml-xs" @click.stop="deleteIt(session.id)" />
        </q-item-section>
      </q-item>

      <q-item clickable v-ripple @click="add()">
        <q-item-section avatar>
          <q-icon color="primary" name="add" />
        </q-item-section>
        <q-item-section>
          <q-item-label> 添加对话 </q-item-label>
        </q-item-section>
      </q-item>

      <q-item clickable v-ripple @click="complainDialogRef?.show()">
        <q-item-section avatar>
          <q-icon color="primary" name="send" />
        </q-item-section>
        <q-item-section>
          <q-item-label> 反馈 </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
    <q-space />
    <complain-dialog ref="complainDialogRef" />
    <q-space />

    <q-chip clickable @click="toGroup" color="primary" text-color="white" icon="groups">
      <span class="chip-text">加入群组</span>
    </q-chip>
  </div>
</template>

<script setup lang="ts">
import { ChatSession, addSession, deleteSession, getMySessions } from "@/api/chat";
import emitter from "@/utils/bus";
import { Dialog } from "quasar";
import ComplainDialog from "@/components/chat/ComplainDialog.vue";
import { useUserStore } from "@/store/user";

const $router = useRouter();
const $route = useRoute();
const userStore = useUserStore();

const sessions = ref<ChatSession[]>([]);
const selectedId = ref<int | undefined>(undefined);

const complainDialogRef = ref<InstanceType<typeof ComplainDialog>>();

const isUserMe = (user_id: int) => {
  return user_id === userStore.user?.id;
};

onMounted(async () => {
  try {
    sessions.value = await getMySessions();
  } catch (e) {
    console.log("Not logged in");
  }
});

function selectSession(sessionId: int) {
  selectedId.value = sessionId;
  $router.replace({ name: "chat" });
  emitter.emit("session-changed", sessionId);
}

async function add() {
  try {
    const response = await addSession("");
    sessions.value = await getMySessions();
    selectSession(response.id);
  } catch (error) {
    console.log("添加失败", error);
  }
}

async function deleteIt(chatId: int) {
  try {
    const shouldDelete = await showDeleteConfirmation();
    if (shouldDelete) {
      const response = await deleteSession(chatId);
      sessions.value = await getMySessions();
      if (chatId == selectedId.value) {
        if (sessions.value.length > 0) {
          selectSession(sessions.value[0].id);
        }
      }
    }
  } catch (error) {
    console.error("Error deleting sessions:", error);
    throw error;
  }
}

async function showDeleteConfirmation() {
  return new Promise((resolve, reject) => {
    Dialog.create({
      title: "确认删除",
      message: "确定要删除该会话吗？",
      ok: {
        label: "确认",
        color: "green-6",
      },
      cancel: {
        label: "取消",
        color: "red-6",
      },
    })
      .onOk(() => resolve(true))
      .onCancel(() => resolve(false))
      .onDismiss(() => reject(new Error("Confirmation dialog dismissed.")));
  });
}
function toGroup() {
  window.location.href =
    "http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hAp4a2qh6WwF2GFgK8ZZuBYHYSEZKCm3&authKey=UPNvIpsPZm%2FnH7VA%2BNWk8jk8XESHeJP11f%2FBiAF%2FVD%2BPS0gcaYV7ne5L1PHhf10V&noverify=0&group_code=871493533";
}
emitter.on("session-title-changed", ({ id, title }) => {
  const session = sessions.value.find((t) => t.id == id);
  if (session) session.title = title;
});
</script>

<style scoped>
.q-item-selected {
  background-color: #f0f0f0; /* 修改选中项的背景颜色 */
  font-weight: bold; /* 修改选中项的字体加粗 */
}
.centered-section {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
