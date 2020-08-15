import axios from 'axios'

const state = {
  rosterList: [],
  squadronList: [],
  hqs: [],
  dcsModules: [],
  schedule: [],
}

const mutations = {
  setRoster(state, roster) {
    state.rosterList = roster
  },
  setSquadrons(state, squadrons) {
    state.squadronList = squadrons
  },
  setHQs(state, HQs) {
    state.hqs = HQs
  },
  setDcsModules(state, modules) {
    state.dcsModules = modules
  },
  setSchedule(state, schedule) {
    state.schedule = schedule
  },
}

const getters = {
  roster: (state) => state.rosterList,
  squadrons: (state) => state.squadronList,
  hqs: (state) => state.hqs,
  dcsModules: (state) => state.dcsModules,
  schedule: (state) => state.schedule,
}

const actions = {
  async getRoster({ commit }) {
    const response = await axios.get('/api/roster/aviators/list')
    commit('setRoster', response.data)
  },
  async getSquadrons({ commit }) {
    const response = await axios.get('/api/roster/squadrons/list')
    commit('setSquadrons', response.data)
  },
  async getHQs({ commit }) {
    const response = await axios.get('/api/roster/hqs/list/')
    commit('setHQs', response.data)
  },
  async getDcsModules({ commit }) {
    const response = await axios.get('/api/roster/modules/list/')
    commit('setDcsModules', response.data)
  },
  async getSchedule({ commit }) {
    const response = await axios.get('api/roster/event/list/')
    commit('setSchedule', response.data)
  },
}

export default {
  state,
  mutations,
  getters,
  actions,
}
