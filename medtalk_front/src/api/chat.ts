import api from "./request";
import { UserPartial } from "./user";
import { Page, Pagination, castPagination } from "./page";
import { SharedLink } from "./share";

export enum MessageType {
  Question = 0,
  Answer = 1,
  Note = 2,
}

export interface ChatMessage {
  chat_id: int;
  type: MessageType;
  content: string;
  remark: string;
  id: int;
  send_time: string;
  own_feedback?: ChatFeedback;
}

export interface ChatSession {
  user_id: int;
  id: int;
  title: string;
  delete_time: string;
  create_time: string;
  update_time: string;
  messages?: ChatMessage[];
  user: UserPartial;
  link?: SharedLink;
}

export interface ChatFeedbackUpdate {
  msg_id: int;
  mark_like?: boolean;
  mark_dislike?: boolean;
  content?: string;
}

export interface ChatFeedback {
  msg_id: int;
  user_id: int;
  mark_like: boolean;
  mark_dislike: boolean;
  content: string;
  update_time: string;
}

export interface ChatFeedbackDetailed extends ChatFeedback {
  msg: ChatMessage;
  user: UserPartial;
}

export type ChatStats = {
  total_chats: int;
  total_messages: int;
  total_chats_today: int;
  total_messages_today: int;
  total_chats_yesterday: int;
  total_messages_yesterday: int;
  by_date: { date: string; total_chats: int; total_messages: int; questions: int; answers: int; notes: int }[];
};

// done
export async function getMySessions() {
  return (await api.get<ChatSession[]>("/chat/me")).data;
}

export async function deleteSession(chat_id: int) {
  return (await api.delete(`/chat/${chat_id}`)).data;
}

// done
export async function addSession(title: string) {
  return (await api.post<ChatSession>("/chat/", { title })).data;
}

// done
export async function getSessionDetails(chat_id: int) {
  return (await api.get<ChatSession>(`/chat/${chat_id}`)).data;
}

// done
export async function sendQuestion(chat_id: int, question_data: any) {
  return (await api.post<ChatMessage[]>(`/chat/${chat_id}`, question_data)).data;
}

export async function getAllSessions(page: Pagination) {
  const params = castPagination(page);
  return (await api.get<Page<ChatSession>>("/chat/", { params })).data;
}

export async function addFeedback(feedback_data: ChatFeedbackUpdate) {
  return (await api.put<ChatFeedback>("/feedbacks/", feedback_data)).data;
}

export async function getAllFeedbacks(page: Pagination) {
  const params = castPagination(page);
  return (await api.get<Page<ChatFeedbackDetailed>>("/feedbacks/", { params })).data;
}

export async function updateTitle(chat_id: int, new_title: string) {
  return (await api.put<ChatSession>(`/chat/${chat_id}`, { title: new_title })).data;
}

export async function addNote(chat_id: int, content: string, remark: string) {
  return (await api.post<ChatMessage>(`/chat/${chat_id}/note`, { content, remark })).data;
}

export async function getChatStats() {
  return (await api.get<ChatStats>("/chat/stat")).data;
}
