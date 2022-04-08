import { createApp, h } from "vue";
import App from "./App.vue";
import router from "./router";
import { store } from "./store";
import vuetify from "@/plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";

loadFonts();

createApp({
  created() {
    const token = localStorage.getItem("token");
    if (token) {
      let parsedToken = JSON.parse(token);
      this.$store.commit("setToken", parsedToken);
      if (!this.$store.getters.tokenExpired) {
        setTimeout(() => {
          this.$store.dispatch("getUser");
        }, 1000);
      } else {
        this.$store.dispatch("logout");
      }
    }
  },
  render: () => h(App),
})
  .use(router)
  .use(store)
  .use(vuetify)
  .mount("#app");
