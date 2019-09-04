import Vue from 'vue'
import App from './App.vue'
import Vuex from  'vuex'
import vuetify from './plugins/vuetify';
import io from 'socket.io-client'

Vue.config.productionTip = false;

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app');

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
    increment (state) {
      state.count ++
    }
  }

});
