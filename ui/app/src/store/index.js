import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentJWT: ''
  },
  getters: {
    jwt: state => state.currentJWT,
    jwtData: (state, getters) => state.currentJWT ? JSON.parse(atob(getters.jwt.split('.')[1])) : null,
    jwtSubject: (state, getters) => getters.jwtData ? getters.jwtData.sub : null,
    jwtIssuer: (state, getters) => getters.jwtData ? getters.jwtData.iss : null
  },
  mutations: {
    setJWT(state, jwt) {
      state.currentJWT = jwt
    }
  },
  actions: {
    async fetchJWT ({ commit }, { username, password }) {
      const response = await axios.post(`http://${location.hostname}/api/token_auth/token/`, {username, password})
      commit('setJWT', response.data)
    }
   },
  modules: {
  }
})
