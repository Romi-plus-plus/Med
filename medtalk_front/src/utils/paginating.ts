import { Page, Pagination } from "@/api/page";
import { TablePagination, TableRequestProps } from "@/typing/quasar";
import { QTable } from "quasar";
import { Ref } from "vue";

export function addSSP(tableRef: Ref<QTable | undefined>) {
  return () => tableRef.value!.requestServerInteraction();
}

export function makePageScope<T>() {
  const pagination = ref<TablePagination>({
    sortBy: null,
    descending: false,
    page: 1,
    rowsPerPage: 20,
    rowsNumber: 0,
  }); // It MUST be REF!
  const loading = ref(false);
  const filter = ref("");
  const rows = ref<T[]>([]);
  return { rows, pagination, loading, filter };
}

export function makeRequester<T>(
  scope: { rows: Ref<T[]>; pagination: Ref<TablePagination>; loading: Ref<boolean> },
  getter: (pg: Pagination) => Promise<Page<T>>
) {
  return async function (prop: TableRequestProps) {
    scope.loading.value = true;
    const res = await getter(prop.pagination);
    scope.rows.value = res.items;
    scope.pagination.value = {
      rowsNumber: res.total,
      page: res.page,
      rowsPerPage: res.size,
      sortBy: prop.pagination.sortBy,
      descending: prop.pagination.descending,
    };
    scope.loading.value = false;
  };
}
