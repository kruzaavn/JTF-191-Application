import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import vuetify from './plugins/vuetify'
import MarkdownItVue from 'markdown-it-vue'
import 'markdown-it-vue/dist/markdown-it-vue.css'

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
        setTimeout(() => {
          this.$store.dispatch('getUser')
        }, 1000)
      } else {
        this.$store.dispatch('logout')
      }
    }
  },
  render: (h) => h(App),
}).$mount('#app')

Vue.use(MarkdownItVue)
