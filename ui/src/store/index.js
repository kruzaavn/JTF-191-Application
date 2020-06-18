import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
    INCREMENT_COUNT (state) {
      state.count++
    }
  },
  actions: {
    increment (context) {
      context.commit('INCREMENT_COUNT')
    }
   },
  modules: {
  }
})
