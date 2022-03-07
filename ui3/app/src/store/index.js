import { createStore } from "vuex";
import authModule from "./modules/authModual";
import gciModule from "./modules/gciModule";
import rosterModule from "./modules/rosterModule";

export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    authModule,
    gciModule,
    rosterModule,
  },
});
