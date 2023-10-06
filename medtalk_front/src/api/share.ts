import { Page, Pagination, castPagination } from "./page";
import api from "./request";

export interface SharedLink {
  create_time: string;
  expire_time: string;
  max_uses: int;
  use_times: int;
  readonly: boolean;
  valid: boolean;
  id: string;
}

export async function createShare(share_data: { chat_id: int; expire_days: int; max_uses: int; readonly: boolean }) {
  return (await api.post<SharedLink>("/share/", share_data)).data;
}

export async function deleteShare(id: string) {
  return (await api.delete<SharedLink>(`/share/${id}`)).data;
}

export async function accessShare(id: string) {
  return (await api.get<SharedLink>(`/share/${id}`)).data;
}

export async function updateShare(id: string, payload: { max_uses?: int; readonly?: boolean; valid?: boolean }) {
  return (await api.put<SharedLink>(`/share/${id}`, payload)).data;
}

export async function getAllShares(page: Pagination) {
  const params = castPagination(page);
  return (await api.get<Page<SharedLink>>(`/share/`, { params })).data;
}
