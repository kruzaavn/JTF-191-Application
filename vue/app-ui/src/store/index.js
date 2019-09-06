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
    dcs: {}
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
      state.dcs = JSON.parse(message.data);
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