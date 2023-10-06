import { date } from "quasar";

export function formatDate(dat: string | null) {
  return dat ? date.formatDate(new Date(dat), "YYYY-MM-DD HH:mm:ss") : "";
}

export function formatNow() {
  return date.formatDate(new Date(), "YYYY-MM-DD HH:mm:ss");
}

export function formatDateToDay(dat: string) {
  return date.formatDate(new Date(dat), "YYYY-MM-DD");
}
