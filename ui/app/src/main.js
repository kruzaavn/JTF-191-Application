import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

new Vue({
  store,
  router,
  vuetify,
  created() {
    const token = localStorage.getItem('token')
    if (token) {
      let parsedToken = JSON.parse(token)
      this.$store.commit('setToken', parsedToken)
      if (!this.$store.getters.tokenExpired) {
        this.$store.dispatch('getUser')
      } else {
        this.$store.dispatch('logout')
      }

    }
  },
  render: (h) => h(App),
}).$mount('#app')
