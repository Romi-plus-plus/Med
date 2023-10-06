import api from "./request";

type Counter = { [key: string]: int };

export type QuestionStats = {
  word: Counter;
  intent: Counter;
  entity: Counter;
};

export async function getQuestionStats() {
  return (await api.get<QuestionStats>("/questions/stat")).data;
}
