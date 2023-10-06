import mitt from "mitt";

type Events = {
  "session-changed": int;
  "session-title-changed": { id: int; title: string };
};

const emitter = mitt<Events>();

export default emitter;
