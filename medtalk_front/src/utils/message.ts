import { Notify } from "quasar";

const Message = {
  success: (message: string) => Notify.create({ type: "positive", message }),
  warning: (message: string) => Notify.create({ type: "warning", message }),
  error: (message: string) => Notify.create({ type: "negative", message }),
  info: (message: string) => Notify.create({ type: "info", message }),
};

export default Message;
