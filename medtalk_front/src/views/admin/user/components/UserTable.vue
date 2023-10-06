<template>
  <q-table
    ref="tableRef"
    title="用户管理"
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
    <template v-for="(val, key) in metadata" #[`body-cell-${key}`]="props">
      <q-td :props="props">
        <template v-if="val.chip">
          <q-chip dense :icon="val.chip" color="transparent">
            {{ val.chip == "access_time" ? formatDate(props.row[key]) : props.row[key] }}
          </q-chip>
        </template>
        <template v-else>
          {{ props.row[key] }}
        </template>
        <template v-if="val.editable">
          &thinsp;<q-icon name="o_edit" color="green" size="8px" />
          <q-popup-edit v-model="props.row[key]" v-slot="scope">
            <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
          </q-popup-edit>
        </template>
      </q-td>
    </template>
    <template #body-cell-is_superuser="props">
      <q-td :props="props">
        <q-checkbox
          dense
          v-model="props.row.is_superuser"
          checked-icon="star"
          unchecked-icon="star_border"
          indeterminate-icon="help"
          color="red"
          :disable="true"
        />
      </q-td>
    </template>
    <template #body-cell-valid="props">
      <q-td :props="props">
        <q-checkbox dense size="sm" v-model="props.row.valid" />
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
import { User, getUsers, updateUser } from "@/api/user";
import { TablePagination } from "@/typing/quasar";
import { formatDate } from "@/utils/date-utils";
import Message from "@/utils/message";
import { addSSP, makeRequester } from "@/utils/paginating";
import { columnDefaults } from "@/utils/table-utils";
import { QTable } from "quasar";

const columns = columnDefaults(
  [
    { name: "id", label: "ID" },
    { name: "username", label: "用户名" },
    { name: "email", label: "邮箱" },
    { name: "phone", label: "电话" },
    { name: "name", label: "姓名" },
    { name: "create_time", label: "注册时间", format: formatDate },
    { name: "update_time", label: "更新时间", format: formatDate },
    { name: "login_time", label: "登录时间", format: formatDate },
    { name: "is_superuser", label: "是否为超级用户" },
    { name: "valid", label: "有效" },
    { name: "handle", label: "操作", sortable: false },
  ],
  { sortable: true, align: "center" }
);
const metadata: { [key: string]: { editable?: boolean; chip?: string } } = {
  username: { editable: true },
  email: { editable: true, chip: "email" },
  phone: { editable: true, chip: "phone" },
  name: { editable: true },
  create_time: { chip: "access_time" },
  update_time: { chip: "access_time" },
  login_time: { chip: "access_time" },
};

const rows = ref<User[]>([]);

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

const onRequest = makeRequester({ rows, pagination, loading }, getUsers);

async function onUpdateEdit(user: User) {
  const res = await updateUser(user.id, user);
  Object.assign(user, res);
  Message.success("成功编辑用户信息");
}
</script>

<style scoped>
.q-table .q-chip {
  font-size: 13px;
}
</style>
