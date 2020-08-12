import axios from 'axios'

// namespaced: true,
const state = {
  currentJWT: JSON.parse(localStorage.getItem('token')),
  username: localStorage.getItem('username'),
}

const mutations = {
  setJWT(state, jwt) {
    state.currentJWT = jwt
    localStorage.setItem('token', JSON.stringify(jwt))
    },
    setJWTAccess(state, access) {
        state.currentJWT.access = access
        localStorage.setItem('token', JSON.stringify(state.currentJWT))
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
  async fetchJWT({ commit, getters }, { username, password }) {
    const response = await axios.post('/api/token_auth/token/', {
      username: username,
      password: password,
    })
    commit('setJWT', response.data)
    commit('setUsername', username)

      axios.defaults.headers.common.Authorization = `Bearer ${getters.jwtAccess}`
      axios.interceptors.response.use(function (response) {
        // Any status code that lie within the range of 2xx cause this function to trigger
        return response;
      }, function (error) {
        // Any status codes that falls outside the range of 2xx cause this function to trigger


          if (error.response.status === 401 && error.response.data.code === "token_not_valid") {

              axios.post('/api/token_auth/refresh/', {refresh: getters.jwtRefresh}).then(response => {
                  commit('setJWTAccess', response.data.access)
                  axios.defaults.headers.common.Authorization = `Bearer ${getters.jwtAccess}`
              })

              return axios(error.config)
          }

        return Promise.reject(error);
      })
    },
    async refreshJWT ({commit, getters}) {

      const response = await axios.post('/api/token_auth/refresh/', {refresh: getters.jwtRefresh})
      commit('setJWTAccess', response.data.access)
      axios.defaults.headers.common.Authorization = `Bearer ${getters.jwtAccess}`
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
