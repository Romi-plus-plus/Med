<template>
  <q-dialog v-model="visible" persistent>
    <q-card style="min-width: 600px;min-height=600px">
      <q-card-section>
        <div class="text-h6" style="display: flex; align-items: center">
          <span style="flex: 1">您的反馈</span>
          <q-btn-dropdown color="primary" :label="complain_type" style="margin-left: auto">
            <q-list>
              <q-item clickable v-close-popup @click="onItemClick('信息不准确')">
                <q-item-section>
                  <q-item-label>信息不准确</q-item-label>
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup @click="onItemClick('信息不完整')">
                <q-item-section>
                  <q-item-label>信息不完整</q-item-label>
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup @click="onItemClick('响应时间长')">
                <q-item-section>
                  <q-item-label>响应时间长</q-item-label>
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup @click="onItemClick('其他问题')">
                <q-item-section>
                  <q-item-label>其他问题</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-input
          type="textarea"
          style="min-height=600px"
          v-model="report_detail.content"
          filled
          color="white"
          @keyup.enter="visible = false"
        />
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="取消" v-close-popup />
        <q-btn flat label="确认" v-close-popup @click="addComplain" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { postComplaint } from "@/api/complaint";
import Message from "@/utils/message";

const visible = ref(false);

let complain_type = ref("");
let report_detail = ref({
  content: "",
  category: "",
});

function onItemClick(type: string) {
  complain_type.value = type;
}

async function addComplain() {
  if (report_detail.value.content) {
    try {
      const response = await postComplaint(complain_type.value, report_detail.value.content);
      Message.success("您的反馈是我们前进的动力");
      complain_type.value = "";
      report_detail.value.category = "";
      report_detail.value.content = "";
    } catch (error) {
      Message.error("发送反馈信息失败");
      console.error("Failed to add complain:", error);
    }
  } else {
    Message.warning("请输入完整反馈信息哦");
  }
}

function show() {
  visible.value = true;
}

defineExpose({ show });
</script>

<style scoped></style>
