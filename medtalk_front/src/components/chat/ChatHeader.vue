<template>
  <div>
    <q-input
      bottom-slots
      v-model="session.title"
      counter:dense="dense"
      class="title"
      input-class="input-large"
      @blur="update_title(session.id, session.title)"
      style="font-size: 28px"
      placeholder="新的聊天"
    >
      <template #hint> 编辑文本以更改标题 </template>
      <template #after>
        <q-btn
          flat
          round
          push
          icon="link"
          @click="chatShareDialogRef?.show()"
          :color="session.link?.valid ? 'primary' : undefined"
        />
      </template>
    </q-input>
    <chat-share-dialog ref="chatShareDialogRef" :session="session" />

    <div class="row">
      <q-chip outline color="primary" text-color="white" icon="event">
        创建时间 | {{ formatDate(session.create_time) }}
      </q-chip>
      <q-chip outline color="primary" text-color="white" icon="event">
        更新时间 | {{ formatDate(session.update_time) }}
      </q-chip>
      <q-space />
      <q-chip outline color="primary" text-color="white" icon="person">
        {{ session.user.username }}
      </q-chip>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChatSession, updateTitle } from "@/api/chat";
import ChatShareDialog from "@/components/chat/ChatShareDialog.vue";
import emitter from "@/utils/bus";
import { formatDate } from "@/utils/date-utils";

const props = defineProps<{ session: ChatSession }>();
const chatShareDialogRef = ref<InstanceType<typeof ChatShareDialog>>();

async function update_title(chat_id: int, title: string) {
  if (title !== "") {
    emitter.emit("session-title-changed", { id: chat_id, title });
    const titleWithoutTags = title.replace(/<a>|<\/a>/gi, "");
    const response = await updateTitle(chat_id, titleWithoutTags);
    Object.assign(props.session, response);
  }
}
</script>

<style scoped></style>
