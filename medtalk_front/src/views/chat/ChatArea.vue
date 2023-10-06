<template>
  <div class="q-pa-md" ref="dialogContainerRef">
    <q-layout view="hHh lpR fFf">
      <q-page-container>
        <q-page v-if="session" class="q-pa-lg">
          <chat-header :session="session" />

          <div class="q-pa-md">
            <q-chat-message
              name="medbot"
              avatar="/img/chatbot.jpg"
              :text="[
                '您好！我是Med，您的AI小助手。请告诉我你希望我帮忙的问题。',
                '您可以这么问我：为什么我的设备不运行？',
              ]"
              :stamp="formatDate(session.create_time)"
            />
            <my-chat-message v-for="group in messagesGrouped" :key="group[0].id" :messages="group" />
          </div>
          <chat-input ref="inputRef" :session="session" @message-sent="sendMessage" />
        </q-page>
      </q-page-container>
      <q-drawer side="right" v-model="drawerRight" show-if-above :width="300" :breakpoint="700" bordered>
        <q-scroll-area class="fit pt-16">
          <div class="q-pa-sm">
            <recommend-list @send="sendRecommend" />
          </div>
        </q-scroll-area>
        <!-- <q-fab
          v-model="fabLeft"
          vertical-actions-align="left"
          color="primary"
          glossy
          icon="keyboard_arrow_up"
          direction="up"
          class="fixed bottom-1 right-32"
        >
          <q-fab-action
            label-position="right"
            color="primary"
            icon="note"
            label="笔记"
            @click="noteDialogRef?.show()"
          />
          <q-fab-action label-position="right" color="primary" icon="note" label="显示当前会话笔记" />
        </q-fab> -->
        <chat-note-list :notes="notes" />
        <complain-dialog ref="complainDialogRef" />
        <chat-note-dialog v-if="session" ref="noteDialogRef" :session="session" />
      </q-drawer>
    </q-layout>
  </div>
</template>

<script setup lang="ts">
import { ChatMessage, ChatSession, MessageType, getSessionDetails, updateTitle } from "@/api/chat";
import MyChatMessage from "@/components/chat/MyChatMessage.vue";
import RecommendList from "@/components/chat/RecommendList.vue";
import ChatHeader from "@/components/chat/ChatHeader.vue";
import ChatInput from "@/components/chat/ChatInput.vue";
import ComplainDialog from "@/components/chat/ComplainDialog.vue";
import ChatNoteDialog from "@/components/chat/ChatNoteDialog.vue";
import ChatNoteList from "@/components/chat/ChatNoteList.vue";
import { formatDate } from "@/utils/date-utils";
import emitter from "@/utils/bus";
import { date } from "quasar";

const sessionId = ref<int | undefined>(undefined);
const session = ref<ChatSession | undefined>(undefined);

const inputRef = ref<InstanceType<typeof ChatInput>>();
const complainDialogRef = ref<InstanceType<typeof ComplainDialog>>();
const noteDialogRef = ref<InstanceType<typeof ChatNoteDialog>>();

const drawerRight = ref(true);
const fabLeft = ref(true);

const dialogContainerRef = ref<HTMLElement>();

const notes = computed(() => session.value?.messages?.filter((m) => m.type == MessageType.Note));

const loading = ref(false);

// 将相邻的消息打包
const messagesGrouped = computed(() => {
  const groups: ChatMessage[][] = [];
  if (session.value?.messages) {
    for (const m of session.value?.messages) {
      if (m.type === MessageType.Note) continue;
      if (groups.length === 0 || m.type !== groups.at(-1)?.[0].type) {
        groups.push([m]);
      } else {
        groups.at(-1)?.push(m);
      }
    }
  }
  return groups;
});

emitter.on("session-changed", onSessionChanged);

async function onSessionChanged(newValue: int) {
  loading.value = true;
  sessionId.value = newValue;
  const resp = await getSessionDetails(newValue);
  resp.messages?.sort((a, b) => {
    const diff = date.getDateDiff(a.send_time, b.send_time);
    if (diff != 0) return diff;
    return a.id - b.id;
  });
  session.value = resp
  loading.value = false;
}

function sendMessage(messages: ChatMessage[]) {
  session.value?.messages?.push(...messages);
  if (session.value?.title === "") {
    const default_title = messages[0].content.substring(0, 10);
    updateTitle(session.value.id, default_title);
  }
  nextTick(() => {
    dialogContainerRef.value!.scrollTop = dialogContainerRef.value!.scrollHeight;
  });
}

function sendRecommend(title: string) {
  inputRef.value?.manualSend(title);
}
</script>

<style scoped lang="scss"></style>
