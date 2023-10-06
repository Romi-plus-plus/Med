<template>
  <q-table
    grid
    ref="tableRef"
    title="投诉管理"
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
    <template #top-right>
      <q-btn-toggle
        v-model="resolvedFilter"
        push
        :toggle-color="resToggleColor"
        :options="[
          { label: '已处理', value: true, icon: 'task' },
          { label: '待处理', value: false, icon: 'assignment' },
          { label: '全部', value: null, icon: 'list' },
        ]"
        @update:model-value="onToggleChanged"
      />
    </template>
    <template v-slot:item="props">
      <div
        class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
        :style="props.selected ? 'transform: scale(0.95);' : ''"
      >
        <q-card>
          <q-list dense>
            <template v-for="col in props.cols" :key="col.name">
              <q-item v-if="props.row[col.name] !== null">
                <q-item-section style="min-width: 40px">
                  <q-item-label>{{ col.label }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-item-label v-if="col.name == 'category'">
                    <q-badge>{{ col.value }}</q-badge>
                  </q-item-label>
                  <q-item-label v-if="col.name=='content'" >
                    <detail-view :text="props.row.content" :limit="30" />
                  </q-item-label>
                  <q-item-label v-else >{{ col.value }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-list>
          <q-separator />
          <q-card-section v-if="!props.row.resolve_time">
            <q-btn label="处理" color="primary" @click="handleComplaint(props.row)" />
          </q-card-section>
        </q-card>
      </div>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import { Complaint, getAllComplaints, resolveComplaint } from "@/api/complaint";
import { Pagination } from "@/api/page";
import { TablePagination } from "@/typing/quasar";
import { formatDate } from "@/utils/date-utils";
import Message from "@/utils/message";
import { addSSP, makeRequester } from "@/utils/paginating";
import { columnDefaults } from "@/utils/table-utils";
import { QTable } from "quasar";

const $q = useQuasar();

const columns = columnDefaults(
  [
    { name: "id", label: "ID" },
    { name: "user", label: "用户", field: (row: Complaint) => row.user.username },
    { name: "category", label: "分类" },
    { name: "content", label: "内容" },
    { name: "create_time", label: "创建时间", format: formatDate },
    { name: "resolve_time", label: "处理时间", format: formatDate },
    { name: "admin", label: "处理者", field: (row: Complaint) => row.admin?.username },
    { name: "reply", label: "回复" },
  ],
  { sortable: true, align: "center" }
);

const rows = ref<Complaint[]>([]);

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

const resolvedFilter = ref<boolean | null>(false);
const resToggleColor = computed(() => {
  if (resolvedFilter.value === true) return "green";
  else if (resolvedFilter.value === false) return "orange";
  else return "teal";
});

onMounted(addSSP(tableRef));

const getAllComplaintsWrapped = (page: Pagination) => getAllComplaints(page, resolvedFilter.value);

const onRequest = makeRequester({ rows, pagination, loading }, getAllComplaintsWrapped);

async function onToggleChanged(value: boolean | null) {
  tableRef.value?.requestServerInteraction();
}

async function handleComplaint(complaint: Complaint) {
  $q.dialog({
    title: "处理投诉",
    message: "回复处理意见",
    prompt: { model: "", type: "textarea" },
    cancel: true,
    persistent: true,
  }).onOk(async (data) => {
    const res = await resolveComplaint(complaint.id, data);
    Message.success("成功处理用户投诉");
    Object.assign(complaint, res);
  });
}
</script>

<style scoped></style>
