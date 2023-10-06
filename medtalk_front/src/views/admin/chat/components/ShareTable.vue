<template>
  <q-table
    ref="tableRef"
    title="共享链接"
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
    <template #body-cell-id="props">
      <q-td :props="props">
        <q-badge :color="isAccessible(props.row) ? 'cyan-5' : 'red-5'">
          {{ props.row.id }}
        </q-badge>
      </q-td>
    </template>
    <template #body-cell-expire_time="props">
      <q-td :props="props">
        <span
          :class="{ 'text-red-500 text-bold': !date.isBetweenDates(now, props.row.create_time, props.row.expire_time) }"
        >
          {{ formatDate(props.row.expire_time) }}
        </span>
      </q-td>
    </template>
    <template #body-cell-use_times="props">
      <q-td :props="props">
        <span :class="{ 'text-red-500 text-bold': props.row.use_times == props.row.max_uses }">
          {{ props.row.use_times }}
        </span>
      </q-td>
    </template>
    <template #body-cell-readonly="props">
      <q-td :props="props">
        <q-checkbox dense v-model="props.row.readonly" indeterminate-icon="help" />
      </q-td>
    </template>
    <template #body-cell-valid="props">
      <q-td :props="props">
        <q-checkbox dense v-model="props.row.valid" indeterminate-icon="help" />
      </q-td>
    </template>
    <template #body-cell-handle="props">
      <q-td :props="props">
        <q-btn flat dense round color="blue" icon="edit" size="sm" @click="onUpdateEdit(props.row)" />
      </q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import { ChatSession, deleteSession, getAllSessions } from "@/api/chat";
import { SharedLink, getAllShares, updateShare } from "@/api/share";
import { TablePagination } from "@/typing/quasar";
import { formatDate, formatNow } from "@/utils/date-utils";
import Message from "@/utils/message";
import { addSSP, makeRequester } from "@/utils/paginating";
import { columnDefaults } from "@/utils/table-utils";
import { QTable } from "quasar";
import { date } from "quasar";

const columns = columnDefaults(
  [
    { name: "chat_id", label: "会话id" },
    { name: "id", label: "链接id" },
    { name: "create_time", label: "创建时间", format: formatDate },
    { name: "expire_time", label: "到期时间", format: formatDate },
    {
      name: "expire_days",
      label: "期限天数",
      field: (row) => date.getDateDiff(row.expire_time, row.create_time),
      sortable: false,
    },
    { name: "max_uses", label: "共享次数" },
    { name: "use_times", label: "使用次数" },
    { name: "readonly", label: "只读" },
    { name: "valid", label: "有效" },
    { name: "handle", label: "操作", sortable: false },
  ],
  { sortable: true, align: "center" }
);

const editables: string[] = [];

const rows = ref<SharedLink[]>([]);

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

const now = new Date();

onMounted(addSSP(tableRef));

const onRequest = makeRequester({ rows, pagination, loading }, getAllShares);

function isAccessible(share: SharedLink) {
  return date.isBetweenDates(now, share.create_time, share.expire_time) && share.valid;
}

async function onUpdateEdit(share: SharedLink) {
  const res = await updateShare(share.id, share);
  Object.assign(share, res);
  Message.success("成功编辑分享链接信息");
}
</script>

<style scoped></style>
