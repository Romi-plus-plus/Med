<template>
  <q-table
    ref="tableRef"
    title="聊天会话"
    :rows="rows"
    :columns="columns"
    row-key="id"
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
    <template #body-cell-handle="props">
      <q-td :props="props">
        <q-btn flat dense round color="blue" icon="edit" size="sm" @click="onUpdateEdit(props.row)" />
        <q-btn
          v-if="!props.row.delete_time"
          flat
          dense
          round
          color="red"
          icon="delete"
          size="sm"
          @click="onDelete(props.row)"
        />
        <q-btn v-else flat dense round color="green" icon="restore_from_trash" size="sm" @click="onDelete(props.row)" />
      </q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import { ChatSession, deleteSession, getAllSessions } from "@/api/chat";
import { TablePagination } from "@/typing/quasar";
import { formatDate, formatNow } from "@/utils/date-utils";
import Message from "@/utils/message";
import { addSSP, makeRequester } from "@/utils/paginating";
import { columnDefaults } from "@/utils/table-utils";
import { QTable } from "quasar";

const columns = columnDefaults(
  [
    { name: "id", label: "ID" },
    {
      name: "user",
      label: "用户",
      field: (row: ChatSession) => row.user.username,
      sortable: false,
    },
    { name: "title", label: "标题" },
    { name: "create_time", label: "创建时间", format: formatDate },
    { name: "update_time", label: "更新时间", format: formatDate },
    { name: "delete_time", label: "删除时间", format: formatDate },
    { name: "handle", label: "操作", sortable: false },
  ],
  { sortable: true, align: "center" }
);

const editables = ["title"];

const rows = ref<ChatSession[]>([]);

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

const onRequest = makeRequester({ rows, pagination, loading }, getAllSessions);

async function onUpdateEdit(chat: ChatSession) {
  // const res = await update(user.id, user);
  // Object.assign(user, res);
  Message.success("成功编辑用会话信息");
}

async function onDelete(chat: ChatSession) {
  const res = await deleteSession(chat.id);
  Message.success("成功删除会话");
  chat.delete_time = formatNow();
}
</script>

<style scoped></style>
