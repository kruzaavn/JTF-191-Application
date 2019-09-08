import Vue from 'vue'
import Vuex from 'vuex'
import VueNativeSock from "vue-native-websocket";

Vue.use(Vuex);


export const store = new Vuex.Store({
  state: {
    socket: {
      isConnected: false,
      message: '',
      reconnectError: false
    },
    dcs: {current: {}, prev: {}, sim_time: -1}
  },
  getters : {},
  mutations:{
    SOCKET_ONOPEN (state, event)  {
      Vue.prototype.$socket = event.currentTarget;
      state.socket.isConnected = true
    },
    SOCKET_ONCLOSE (state, event)  {
      Vue.prototype.$socket = event.currentTarget;
      state.socket.isConnected = false
    },
    SOCKET_ONERROR (state, event)  {
      console.error(state, event)
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE (state, message)  {
      let dcs_obj;
      dcs_obj = JSON.parse(message.data);


      let key = Object.keys(dcs_obj)[0];

      dcs_obj = dcs_obj[key];

      if (state.dcs.sim_time !== dcs_obj.sim_time) {
        state.dcs.sim_time = dcs_obj.sim_time;
        state.dcs.prev = state.dcs.current;
        state.dcs.current = {};
      }

      state.dcs.current[key] = dcs_obj;
    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
      console.info(state, count)
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    },
  },
  actions : {}
});

Vue.use(VueNativeSock, 'ws://173.234.25.42:8082', {store:store});