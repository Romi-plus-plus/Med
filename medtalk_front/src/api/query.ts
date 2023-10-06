import axios from "./request";

type AnyObject = { [key: string]: any };

export async function query(): Promise<{ data: AnyObject[]; model: AnyObject[] }> {
  return (await axios.get("/query")).data;
}
