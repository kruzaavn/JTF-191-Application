import axios from 'axios'

const state = {

    rosterList: null,
    squadronList: null,
    hqs: null
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
    }
}

const getters = {

    roster: state => state.rosterList,
    squadrons: state => state.squadronList,
    hqs: state => state.hqs
}

const actions = {

    async getRoster ({ commit }) {
        const response = await axios.get('/api/roster/aviators/list')
        commit('setRoster', response.data)
    },
    async getSquadrons ({ commit }) {
        const response = await axios.get('/api/roster/squadrons/list')
        commit('setSquadrons', response.data)
    },
    async getHQs ({ commit }) {
        const response = await axios.get('/api/roster/hqs/list')
        commit('setHQs', response.data)
    },
}

export default {
    state,
    mutations,
    getters,
    actions
}