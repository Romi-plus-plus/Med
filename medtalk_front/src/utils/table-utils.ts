import { QTable } from "quasar";

type Columns = NonNullable<QTable["columns"]>;
type Column = Columns[number];

export function columnDefaults(
  columns: (Omit<Column, "field"> & Partial<Pick<Column, "field">>)[],
  defaults: Partial<Column>
): Columns {
  return columns.map((c) => Object.assign({ field: c.name }, defaults, c));
}
