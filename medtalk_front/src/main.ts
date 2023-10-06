import { AppFullscreen, Dialog, Notify, Quasar } from "quasar";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import pinia from "./store";
import VueCookies from "vue-cookies";

// Import icon libraries
import "@quasar/extras/material-icons/material-icons.css";
import "@quasar/extras/material-icons-outlined/material-icons-outlined.css";

// Import Quasar css
import "quasar/src/css/index.sass";

// Import Popoto css
import "popoto/dist/popoto.min.css";

import "./styles/index.scss";
import "./styles/app.sass";
import "./styles/theme.scss";

const app = createApp(App);
app.use(router).use(pinia);
app.use(Quasar, {
  plugins: { AppFullscreen, Dialog, Notify },
  config: {
    notify: {
      /* look at QuasarConfOptions from the API card */
    },
  },
});
app.use(VueCookies, { expires: "7d" });

app.mount("#app");
