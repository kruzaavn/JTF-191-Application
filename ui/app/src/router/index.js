import Vue from 'vue'
import VueRouter from 'vue-router'
import About from '../views/About.vue'
import GCI from '../views/GCI.vue'
import Qualification from '@/views/Qualification'
import Squadron from '../views/Squadron'
import JoinUs from '../views/JoinUs'
import Schedule from '@/views/Schedule'
import Register from '@/views/Register'
import SquadronList from '@/views/SquadronList'
import Photos from '@/views/Photos'
import Operation from '@/views/Operation'
import OperationList from '@/views/OperationList'

Vue.use(VueRouter)

const title_header = 'JTF-191'

function title(header, title) {
  return `${header} - ${title}`
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Photos,
    meta: {
      title: title(title_header, 'Photos'),
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
  {
    path: '/server',
    name: 'GCI',
    component: GCI,
    meta: {
      title: title(title_header, 'Servers'),
    },
  },
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
    path: '/squadron',
    name: 'SquadronList',
    component: SquadronList,
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
  {
    path: '/qualification/:qualificationModule',
    name: 'Qualification',
    props: true,
    component: Qualification,
    meta: {
      title: title(title_header, 'Qualifications'),
    },
  },
  {
    path: '/register/:id',
    name: 'Register',
    props: true,
    component: Register,
    meta: {
      title: title(title_header, 'Register'),
    },
  },
  {
    path: '/operation',
    name: 'OperationList',
    component: OperationList,
    meta: {
      title: title(title_header, 'Operations'),
    },
  },
  {
    path: '/operation/:operationName',
    name: 'Operation',
    component: Operation,
    props: true,
    meta: {
      title: title(title_header, 'Operations'),
    },
  },
]

function scrollBehavior(to, from, savedPosition) {
  if (savedPosition) {
    return savedPosition
  } else {
    return { x: 0, y: 0 }
  }
}

const router = new VueRouter({
  routes,
  scrollBehavior,
})

export default router
