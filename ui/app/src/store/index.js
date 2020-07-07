import Vue from 'vue'
import Vuex from 'vuex'
import authModule from './modules/authModual'
import gciModule from './modules/gciModule'
import rosterModule from './modules/rosterModule'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    authModule,
    gciModule,
    rosterModule,
  },
})
