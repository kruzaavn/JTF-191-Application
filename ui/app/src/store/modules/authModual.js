import axios from 'axios'

// namespaced: true,
const state = {
  currentJWT: localStorage.getItem('token'),
  username: localStorage.getItem('username'),
}

const mutations = {
  setJWT(state, jwt) {
    state.currentJWT = jwt
    localStorage.setItem('token', jwt)
  },
  setUsername(state, username) {
    state.username = username
    localStorage.setItem('username', username)
  },
  clearJWT(state) {
    state.currentJWT = null
    state.username = null
    localStorage.clear()
  },
}
const actions = {
  async fetchJWT({ commit }, { username, password }) {
    const response = await axios.post('/api/token_auth/token/', {
      username: username,
      password: password,
    })
    commit('setJWT', JSON.stringify(response.data))
    commit('setUsername', username)
  },
  logout({ commit }) {
    commit('clearJWT')
  },
}

const getters = {
  jwt: (state) => state.currentJWT,
  jwtData: (state, getters) =>
    state.currentJWT ? JSON.parse(atob(getters.jwt.split('.')[1])) : null,
  jwtSubject: (state, getters) =>
    getters.jwtData ? getters.jwtData.sub : null,
  jwtIssuer: (state, getters) => (getters.jwtData ? getters.jwtData.iss : null),
  userName: (state) => state.username,
}

export default {
  state,
  getters,
  actions,
  mutations,
}
