import Vue from 'vue'
import Vuex from 'vuex'
import VueNativeSock from "vue-native-websocket";

Vue.use(Vuex);

function process_message(message) {
  let process;
  process = message;
  process = process.replace('}{', '}\n{');
  process = process.split('\n');

  if (process[-1] === '') {

    process[-1].pop()

  }

  return process
}

export const store = new Vuex.Store({
  state: {
    socket: {
      isConnected: false,
      message: '',
      reconnectError: false
    },
    current: {},
    buffer: {},
    sim_time: -1,
    active: {}
  },
  getters : {
    active_pilots: function (state) {

      let active = {};

      for (let id in state.current) {

        if (state.current[id].states.Flags.Human) {

          active[id] = state.current[id]

        }

      }


      return active
    }
  },
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
      let data =  process_message(message.data);

      for (let msg of data) {

        dcs_obj = JSON.parse(msg);
        let key = Object.keys(dcs_obj)[0];

        dcs_obj = dcs_obj[key];

        if (state.sim_time !== dcs_obj.sim_time) {
          state.sim_time = dcs_obj.sim_time;
          state.current = state.buffer;
          state.buffer = {};
        }

        state.buffer[key] = dcs_obj;
        // state.active[key] = dcs_obj;


      }
    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
      console.log(state, count)
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    },
  },
  actions : {}
});





Vue.use(VueNativeSock, 'ws://173.234.25.42:8082', {store:store});