import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Settings from './views/Settings.vue'
import Descriptions from './components/Descriptions.vue'
import Items from './components/Items.vue'

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/settings',
            component: Settings,
            children: [
                {
                    path: 'Items',
                    component: Items,
                    name: 'items',
                },
                {
                    path: ':id',
                    component: Descriptions,
                    name: 'description',
                }
            ]
        },
        {
            path: '*',
            redirect: { name: 'home' }
        }
    ]
})
