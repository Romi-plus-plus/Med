import { Page, Pagination, castPagination } from "./page";
import api from "./request";
import { UserPartial } from "./user";

export interface Recommendation {
  id: int;
  title: string;
  content: string;
  add_time: string;
}

export interface RecommendationMore extends Recommendation {
  remove_time: string;
  creator: UserPartial;
  remover: UserPartial;
}

export async function getRecommendations() {
  return (await api.get<Recommendation[]>("/recommends/")).data;
}

export async function getAllRecommendations(page: Pagination, active?: boolean) {
  const params = { ...castPagination(page), active };
  return (await api.get<Page<RecommendationMore>>("/recommends/all", { params })).data;
}

export async function createRecommendation(title: string, content: string) {
  return (await api.post<RecommendationMore>("/recommends/", { title, content })).data;
}

export async function removeRecommendation(id: int) {
  return (await api.delete<RecommendationMore>(`/recommends/${id}`)).data;
}

export async function recoverRecommendation(id: int) {
  return (await api.put<RecommendationMore>(`/recommends/${id}`)).data;
}
