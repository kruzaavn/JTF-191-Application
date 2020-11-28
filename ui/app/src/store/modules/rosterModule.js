import axios from 'axios'

const state = {
  rosterList: [],
  squadronList: [],
  hqs: [],
  dcsModules: [],
  schedule: [],
  qualificationList: [],
  qualificationModuleList: [],
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
  addEvent(state, event) {
    state.schedule.push(event)
  },
  setQualifications(state, qualifications) {
    state.qualificationList = qualifications
  },
  setQualificationModules(state, modules) {
    state.qualificationModuleList = modules
  },
}

const getters = {
  roster: (state) => state.rosterList,
  squadrons: (state) => state.squadronList,
  hqs: (state) => state.hqs,
  dcsModules: (state) => state.dcsModules,
  schedule: (state) => state.schedule,
  qualifications: (state) => state.qualificationList,
  qualificationModules: (state) => state.qualificationModuleList,
}

const actions = {
  async getRoster({ commit }) {
    const response = await axios.get('/api/roster/aviators/list/')
    commit('setRoster', response.data)
  },
  async getSquadrons({ commit }) {
    const response = await axios.get('/api/roster/squadrons/list/')
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
    const response = await axios.get('/api/roster/event/list/')
    commit('setSchedule', response.data)
  },
  async addToSchedule({commit}, event) {
    const response = await axios.post('/api/roster/event/list/', event)
    commit('addEvent', response.data)
  },
  async getQualifications({ commit }) {
    const response = await axios.get('/api/roster/qualifications/list/')
    commit('setQualifications', response.data)
  },
  async getQualificationModules({ commit }) {
    const response = await axios.get('/api/roster/qualifications/modules/list/')
    commit('setQualificationModules', response.data)
  },
}

export default {
  state,
  mutations,
  getters,
  actions,
}
