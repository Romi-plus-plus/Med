export interface Page<T> {
  /** Items in the requested page */
  items: T[];
  /** Total items */
  total: int;
  /** Page number, from 1 */
  page: int;
  /** Page size */
  size: int;
  /** Total pages */
  pages: int;
}

export interface Pagination {
  sortBy: string;
  descending: boolean;
  page: number;
  rowsPerPage: number;
}

export function castPagination(page: Pagination) {
  return {
    page: page.page,
    size: page.rowsPerPage,
    sort_by: page.sortBy,
    desc: page.descending,
  };
}
