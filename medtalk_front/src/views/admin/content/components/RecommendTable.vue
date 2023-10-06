<template>
  <q-expansion-item expand-icon-toggle expand-separator default-opened icon="list" label="推荐管理">
    <q-table
      grid
      ref="tableRef"
      title=""
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
      <template #top-left>
        <q-btn color="green" icon="add" label="新建" unelevated rounded class="l-shadow-2" @click="dialogShow = true" />
      </template>
      <template #top-right>
        <q-btn-toggle
        v-model="activeFilter"
        push
        :toggle-color="resToggleColor"
        :options="[
          { label: '活跃', value: true, icon: 'recommend' },
          { label: '禁用', value: false, icon: 'block' },
          { label: '全部', value: undefined, icon: 'list' },
        ]"
        @update:model-value="onToggleChanged"
      />
      </template>
      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition">
          <q-card>
            <q-list dense>
              <template v-for="col in props.cols" :key="col.name">
                <q-item v-if="props.row[col.name] !== null">
                  <q-item-section style="min-width: 40px">
                    <q-item-label>{{ col.label }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-item-label v-if="col.name == 'content'">
                      <detail-view :text="props.row.content" :limit="30" />
                    </q-item-label>
                    <q-item-label v-else >{{ col.value }}</q-item-label>
                  </q-item-section>
                </q-item>
              </template>
            </q-list>
            <q-separator />
            <q-card-section>
              <q-btn v-if="!props.row.remove_time" label="移除" color="orange" @click="onRemoveRecommend(props.row)" />
              <q-btn v-if="props.row.remove_time" label="恢复" color="teal" @click="onRecoverRecommend(props.row)" />
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-table>
  </q-expansion-item>

  <q-dialog v-model="dialogShow">
    <q-card style="min-width: 600px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">创建推荐</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-card-section>
        <q-input v-model="newTitle" label="标题" filled dense />
      </q-card-section>
      <q-card-section>
        <q-input v-model="newContent" placeholder="内容" filled autogrow />
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="取消" color="primary" v-close-popup />
        <q-btn flat label="新建" color="primary" v-close-popup @click="onCreateRecommend" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { Pagination } from "@/api/page";
import {
  RecommendationMore,
  createRecommendation,
  getAllRecommendations,
  recoverRecommendation,
  removeRecommendation,
} from "@/api/recommend";
import { TablePagination } from "@/typing/quasar";
import { formatDate } from "@/utils/date-utils";
import Message from "@/utils/message";
import { addSSP, makeRequester } from "@/utils/paginating";
import { columnDefaults } from "@/utils/table-utils";
import { QTable } from "quasar";

// 点击添加按钮，对话框增加

const $q = useQuasar();

const dialogShow = ref(false);
const newTitle = ref("");
const newContent = ref("");

const columns = columnDefaults(
  [
    { name: "id", label: "ID" },
    { name: "title", label: "标题" },
    { name: "content", label: "内容" },
    { name: "creator", label: "创建者", field: (row: RecommendationMore) => row.creator.username },
    { name: "add_time", label: "创建时间", format: formatDate },
    { name: "remover", label: "移除者", field: (row: RecommendationMore) => row.remover.username },
    { name: "remove_time", label: "移除时间", format: formatDate },
  ],
  {}
);

const rows = ref<RecommendationMore[]>([]);

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

const activeFilter = ref<boolean>();
const resToggleColor = computed(() => {
  if (activeFilter.value === true) return "green";
  else if (activeFilter.value === false) return "orange";
  else return "teal";
});

onMounted(addSSP(tableRef));

const getAllRecommendationsWrapped = (page: Pagination) => getAllRecommendations(page, activeFilter.value);

const onRequest = makeRequester({ rows, pagination, loading }, getAllRecommendationsWrapped);

async function onToggleChanged(value: boolean | null) {
  tableRef.value?.requestServerInteraction();
}

async function onCreateRecommend() {
  const res = await createRecommendation(newTitle.value, newContent.value);
  rows.value.splice(0, 0, res);
  Message.success("成功创建推荐");
}

async function onRemoveRecommend(rec: RecommendationMore) {
  const res = await removeRecommendation(rec.id);
  Object.assign(rec, res);
  Message.success("成功移除推荐");
}

async function onRecoverRecommend(rec: RecommendationMore) {
  const res = await recoverRecommendation(rec.id);
  Object.assign(rec, res);
  Message.success("成功恢复推荐");
}
</script>

<style scoped></style>
