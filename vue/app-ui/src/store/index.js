import Vue from 'vue'
import Vuex from 'vuex'
import VueNativeSock from "vue-native-websocket";
import L from 'leaflet'
Vue.use(Vuex);

function process_message(message) {

  const pre_process = message;
  let process = pre_process.replace(new RegExp('\}\{', 'gi'), '}\n{').split('\n');

  if (process[-1] === '') {

    process[-1].pop()

  }

  return process
}


function get_velocity(new_state, old_state) {

  let to = L.latLng([new_state.states.LatLongAlt.Lat, new_state.states.LatLongAlt.Long]);
  let froms = L.latLng([old_state.states.LatLongAlt.Lat, old_state.states.LatLongAlt.Long]);

  let distance = froms.distanceTo(to);
  let vel_kts = Math.round((distance * 3.6 * 0.539957)/10)*10;

  new_state.states.Velocity = vel_kts;

  return new_state


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

          active[id] = state.current[id].states.UnitName

        }

      }

      if (Object.keys(active).length > 0) {
        return active
      } else {return null}
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
      let data = process_message(message.data);

      for (let msg of data) {

          dcs_obj = JSON.parse(msg);
          let key = Object.keys(dcs_obj)[0];

          dcs_obj = dcs_obj[key];

          if (state.sim_time !== dcs_obj.sim_time) {
            state.sim_time = dcs_obj.sim_time;
            state.current = state.buffer;
            state.buffer = {};
          }

          if (key in state.current) {

            dcs_obj = get_velocity(dcs_obj, state.current[key])

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