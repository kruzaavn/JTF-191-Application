import Vue from 'vue';
import VueRouter from 'vue-router'
import GCI from '../components/GCI'
import home from '../components/home'

Vue.use(VueRouter);

export default new VueRouter(
    {
        routes: [
            {
                path: '/',
                name: 'home',
                component: home
            },
            {
                path: '/gci',
                name: 'gci',
                component: GCI
            }
        ]
    }
)