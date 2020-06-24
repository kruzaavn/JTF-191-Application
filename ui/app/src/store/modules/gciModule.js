import axios from 'axios'

const state = {

    serverList: null

}

const mutations = {

    setServers(state, servers) {
        state.serverList = servers
    }
}

const getters = {

    servers: state => state.serverList

}

const actions = {

    async getServers ({ commit }) {
        const response = await axios.get('/api/gci/server/list')
        commit('setServers', response.data)
    }
}

export default {
    state,
    mutations,
    getters,
    actions
}