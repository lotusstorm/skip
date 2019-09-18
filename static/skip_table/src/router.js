import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Settings from './views/Settings.vue'
import Descriptions from './components/Descriptions.vue'
import Items from './components/Items.vue'
import HomeIssues from './components/HomeIssues.vue'

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            // name: 'home',
            component: Home,
            children: [
                {
                    path: '/',
                    component: HomeIssues,
                    name: 'home',
                },
                {
                    path: ':id',
                    component: Descriptions,
                    name: 'home_description',
                }
            ]
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
