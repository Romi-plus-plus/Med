<template>
  <q-dialog v-model="visible">
    <q-card style="min-width: 400px">
      <q-card-section>
        <span class="text-h6">共享链接</span>
        <q-btn v-if="hasLink" dense label="取消分享" class="float-right" @click="cancelShare()" />
        <q-btn v-else dense label="创建" class="float-right" @click="createLink" />
      </q-card-section>
      <q-card-section>
        <div class="row">
          <div class="col-6 q-pa-md">
            <q-select
              v-model="form.expire_days"
              :options="expire_time_options"
              label="有效天数"
              dense
              :disable="hasLink"
            />
          </div>
          <div class="col-6 q-pa-md">
            <q-select
              v-model="form.max_uses"
              :options="max_uses_options"
              label="最多使用次数"
              dense
              :disable="hasLink"
            />
          </div>
        </div>
        <div v-if="hasLink && session.link" class="q-pa-md">
          <q-field dense filled>
            <template #prepend>
              <q-icon name="link" />
            </template>
            <template #control>
              <div class="self-center full-width no-outline" tabindex="0">{{ session.link.id }}</div>
            </template>
            <template v-slot:append>
              <q-btn round dense flat icon="content_copy" @click="copyLink()" ref="copyBtnRef" />
            </template>
          </q-field>
          <div class="text-caption">当前使用次数：{{ session.link.use_times }}</div>
        </div>
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="确认" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ChatSession } from "@/api/chat";
import Message from "@/utils/message";
import { createShare, deleteShare } from "@/api/share";
import useClipboard from "vue-clipboard3";

const { toClipboard } = useClipboard();

const props = defineProps<{ session: ChatSession }>();

const copyBtnRef = ref();

const visible = ref(false);
const expire_time_options = ["1", "3", "7", "10", "30"];
const max_uses_options = ["1", "3", "7", "10", "无限"];
let readonly_model = ref("只可读");

const form = ref({
  expire_days: 1,
  max_uses: props.session.link?.max_uses ?? 1,
  readonly: true,
});

const hasLink = computed(() => Boolean(props.session.link?.valid));

async function createLink() {
  try {
    if (readonly_model.value === "只可读") {
      form.value.readonly = true;
    } else {
      form.value.readonly = false;
    }
    const response = await createShare({
      chat_id: props.session.id,
      expire_days: form.value.expire_days,
      max_uses: form.value.max_uses,
      readonly: form.value.readonly,
    });
    props.session.link = response;
    Message.success("创建共享链接");
  } catch (e) {
    console.log(e);
  }
}

async function cancelShare() {
  const response = await deleteShare(props.session.link!.id);
  props.session.link = response;
  Message.success("取消分享");
}

async function copyLink() {
  if (!props.session.link) return;
  try {
    await toClipboard(props.session.link.id, copyBtnRef.value.$el);
    // 模态框必须传container
    Message.info("复制到剪贴板");
  } catch (e) {
    console.error(e);
  }
}

function show() {
  visible.value = true;
}

defineExpose({ show });
</script>

<style scoped></style>
