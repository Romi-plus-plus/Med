<template>
  <q-dialog v-model="visible" persistent>
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">发布笔记</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-input type="textarea" v-model="noteDetail.content" filled @keyup.enter="visible = false" />
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="取消" v-close-popup />
        <q-btn flat label="确认" v-close-popup @click="addBookNote(session.id)" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ChatSession, addNote } from "@/api/chat";
import Message from "@/utils/message";

const props = defineProps<{ session: ChatSession }>();

const visible = ref(false);

const noteDetail = ref({
  content: "",
  remark: "",
});

async function addBookNote(session_id: int) {
  if (noteDetail.value.content) {
    try {
      const response = await addNote(session_id, noteDetail.value.content, "123");
      Message.success("添加笔记成功");
      noteDetail.value.content = "";
      noteDetail.value.remark = "";
    } catch (error) {
      Message.error("添加笔记失败");
      console.error("Failed to add note:", error);
    }
  } else {
    Message.warning("请添加笔记信息哦");
  }
}

function show() {
  visible.value = true;
}

defineExpose({ show });
</script>

<style scoped></style>
