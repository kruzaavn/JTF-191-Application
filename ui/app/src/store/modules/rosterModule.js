import axios from 'axios'

const state = {
  rosterList: [],
  squadronList: [],
  hqs: [],
  dcsModules: [],
  schedule: [],
  qualificationList: [],
  qualificationModuleList: [],
  photos: [],
  storesList: [],
  munitionList: [],
  operationList: [],
  aviator: {},
  leavesOfAbsence: [],
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
  removeEvent(state, event) {
    const index = state.schedule.findIndex((element) => element.id === event.id)
    state.schedule.splice(index, 1)
  },
  updateEvent(state, event) {
    const index = state.schedule.findIndex((element) => element.id === event.id)
    state.schedule.splice(index, 1, event)
  },
  setQualifications(state, qualifications) {
    state.qualificationList = qualifications
  },
  setQualificationModules(state, modules) {
    state.qualificationModuleList = modules
  },
  setPhotos(state, photos) {
    state.photos = photos
  },
  setMunition(state, munitions) {
    state.munitionList = munitions
  },
  setStores(state, stores) {
    state.storesList = stores
  },
  setOperations(state, operations) {
    state.operationList = operations
  },
  setAviator(state, aviator) {
    state.aviator = aviator
  },
}

const getters = {
  roster: (state) => state.rosterList,
  squadrons: (state) => state.squadronList,
  hqs: (state) => state.hqs,
  aviator: (state) => state.aviator,
  dcsModules: (state) => state.dcsModules,
  schedule: (state) => state.schedule,
  qualifications: (state) => state.qualificationList,
  qualificationModules: (state) => state.qualificationModuleList,
  photos: (state) => state.photos,
  munitions: (state) => state.munitionList,
  stores: (state) => state.storesList,
  leavesOfAbsence: (state) => state.leavesOfAbsence,
  munitionsTable: (state) => {
    let table = state.storesList.reduce((acc, element) => {
      const previous = acc.find(
        (x) =>
          x.munition === element.munition && x.squadron === element.squadron
      )

      if (previous) {
        previous.count += element.count
      } else {
        const munition = state.munitionList.find(
          (x) => x.id === element.munition
        )
        element.munition_name = munition.name
        element.munition_type = munition.munition_type
          .replaceAll('_', ' ')
          .toUpperCase()
        element.squadron_name = state.squadronList.find(
          (x) => x.id === element.squadron
        ).name
        acc.push(element)
      }
      return acc
    }, [])

    return table
  },
  operations: (state) => {
    return state.operationList
  },
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
  async getSchedule({ commit }, date) {
    const response = await axios.get(`/api/roster/event/list/${date.start}/${date.end}/`)
    commit('setSchedule', response.data)
  },
  async addToSchedule({ commit }, event) {
    const response = await axios.post('/api/roster/event/list/', event)
    commit('addEvent', response.data)
  },
  async updateSchedule({ commit }, event) {
    const response = await axios.put(
      `/api/roster/event/detail/${event.id}/`,
      event
    )
    commit('updateEvent', response.data)
  },
  async removeFromSchedule({ commit }, event) {
    await axios.delete(`/api/roster/event/detail/${event.id}/`)
    commit('removeEvent', event)
  },
  async getQualifications({ commit }) {
    const response = await axios.get('/api/roster/qualifications/list/')
    commit('setQualifications', response.data)
  },
  async getQualificationModules({ commit }) {
    const response = await axios.get('/api/roster/qualifications/modules/list/')
    commit('setQualificationModules', response.data)
  },
  async getPhotos({ commit }) {
    const response = await axios.get('/api/roster/user_images/list/')
    commit('setPhotos', response.data)
  },
  async getMunitionsList({ commit }) {
    const response = await axios.get('/api/roster/munition/list/')
    commit('setMunition', response.data)
  },
  async getStoresList({ commit }, operationName) {
    const response = await axios.get(
      `/api/roster/stores/list/${operationName}/`
    )
    commit('setStores', response.data)
  },
  async getOperations({ commit }) {
    const response = await axios.get('/api/roster/operation/list')
    commit('setOperations', response.data)
  },
  async getAviatorFromUser({ commit }, userId) {
    const token = localStorage.getItem('token')
    const config = {
      headers: { Authorization: `Bearer ${token}` }
    }
    const response = await axios.get(
      `/api/roster/aviators/fromuser/${userId}/`,
      {},
      config
    )
    commit('setAviator', response.data)
  },
}

export default {
  state,
  mutations,
  getters,
  actions,
}
