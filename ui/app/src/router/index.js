import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
// import GCI from '../views/GCI.vue'
import Squadron from '../views/Squadron'
import JoinUs from '../views/JoinUs'
import Schedule from '@/views/Schedule'

Vue.use(VueRouter)

const title_header = 'JTF-191'

function title(header, title) {
  return `${header} - ${title}`
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: title(title_header, 'Home'),
    },
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: {
      title: title(title_header, 'About Us'),
    },
  },
  // 11/1/2020 removing WEB GCI
  // {
  //   path: '/gci',
  //   name: 'GCI',
  //   component: GCI,
  //   meta: {
  //     title: title(title_header, 'GCI'),
  //   },
  // },
  {
    path: '/squadron/:squadronDesignation',
    name: 'Squadron',
    component: Squadron,
    props: true,
    meta: {
      title: title(title_header, 'Squadrons'),
    },
  },
  {
    path: '/joinus',
    name: 'JoinUs',
    component: JoinUs,
    meta: {
      title: title(title_header, 'Join Us'),
    },
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: Schedule,
    meta: {
      title: title(title_header, 'Schedule'),
    },
  },
]

const router = new VueRouter({
  routes,
})

export default router
