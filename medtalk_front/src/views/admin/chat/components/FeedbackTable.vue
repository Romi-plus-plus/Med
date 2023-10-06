<template>
  <q-table
    ref="tableRef"
    title="聊天消息反馈"
    :rows="rows"
    :columns="columns"
    row-key="id"
    binary-state-sort
    square
    flat
    dense
    class="my-sticky-table-handle"
    :filter="filter"
    :loading="loading"
    v-model:pagination="pagination"
    @request="onRequest"
  >
    <template v-for="field in editables" #[`body-cell-${field}`]="props">
      <q-td :props="props">
        {{ props.row[field] }}
        <q-popup-edit v-model="props.row[field]" v-slot="scope">
          <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
        </q-popup-edit>
      </q-td>
    </template>
    <template #body-cell-msg="props">
      <q-td :props="props">
        <detail-view :text="props.row.msg.content" :limit="10" />
      </q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import { ChatFeedbackDetailed, getAllFeedbacks } from "@/api/chat";
import { User, updateUser } from "@/api/user";
import { TablePagination } from "@/typing/quasar";
import { formatDate } from "@/utils/date-utils";
import Message from "@/utils/message";
import { addSSP, makeRequester } from "@/utils/paginating";
import { columnDefaults } from "@/utils/table-utils";
import { QTable } from "quasar";

const columns = columnDefaults(
  [
    { name: "user", label: "用户", field: (row: ChatFeedbackDetailed) => row.user.username },
    {
      name: "msg",
      label: "消息",
      field: (row: ChatFeedbackDetailed) => row.msg.content,
    },
    { name: "mark_like", label: "👍", format: (val) => (val ? "👍" : "") },
    { name: "mark_dislike", label: "👎", format: (val) => (val ? "👎" : "") },
    { name: "content", label: "评论" },
    { name: "update_time", label: "反馈时间", format: formatDate },
  ],
  { sortable: true, align: "center" }
);

const editables = ["content"];

const rows = ref<ChatFeedbackDetailed[]>([]);

const tableRef = ref<QTable>();

const pagination = ref<TablePagination>({
  sortBy: null,
  descending: false,
  page: 1,
  rowsPerPage: 20,
  rowsNumber: 0,
}); // It MUST be REF!

const loading = ref(false);
const filter = ref("");

onMounted(addSSP(tableRef));

const onRequest = makeRequester({ rows, pagination, loading }, getAllFeedbacks);

/*TODO*/
async function onUpdateEdit(user: User) {
  const res = await updateUser(user.id, user);
  Object.assign(user, res);
  Message.success("成功编辑用户信息");
}
</script>

<style scoped></style>
