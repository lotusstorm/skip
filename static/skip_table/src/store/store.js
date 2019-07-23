import Vue from 'vue'
import Vuex from 'vuex'

import db from './modules/db'
import render from './modules/render'


Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        db,
        render
    }
})
