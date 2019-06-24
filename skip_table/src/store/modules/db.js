import { HTTP } from '../globalSettings'


const state = {
    tests: [],
    steps: [],
    bugs: [],
    modules: [],

    notRenderBugs: ['qa.Closed', 'dev.Closed', 'dev.Resolved', 'qa.Resolved']
};

const mutations = {
    setTests: (state, tests) => {
        state.tests = tests
    },

    setSteps: (state, steps) => {
        state.steps = steps
    },

    setBugs: (state, bugs) => {
        bugs.forEach(el => el['bind'] = false);
        state.bugs = bugs.sort(i => i['id']).reverse()
    },

    setModules: (state, modules) => {
        state.modules = modules
    },
};

const actions = {
    loadTests: ({commit}, value) => {
        HTTP.post("/tests", {
                branch: value
            })
            .then((response) => {
                commit('setTests', response.data.data);
                console.log(response.data.data);
                Promise.resolve()
                // console.log(value);
                // this.tests_r = this.tests.filter(i => i['id'] > 0);
            })
            .catch((error) => {
                console.log(value);
                console.log(error);
                console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
            });

    },

    loadSteps: ({commit}, value) => {
        HTTP.post("/steps", {
                branch: value
            })
            .then((response) => {
                commit('setSteps', response.data.data);
                // console.log(response.data.data);
                // console.log(value);
                // this.tests_r = this.tests.filter(i => i['id'] > 0);
            })
            .catch((error) => {
                console.log(value);
                console.log(error);
                console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
            });
    },

    loadBugs: ({commit}) => {
        HTTP.get("/bugs")
            .then((response) => {
                commit('setBugs', response.data.data);
                // this.tests_r = this.tests.filter(i => i['id'] > 0);
                console.log(response.data.data)
            })
            .catch((error) => {
                console.log(error);
                console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
            });
    },

    loadModules: ({commit}, value) => {
        HTTP.post("/modules", {
                branch: value
            })
            .then((response) => {
                commit('setModules', response.data.data);
                // this.tests_r = this.tests.filter(i => i['id'] > 0);
                // console.log(response.data.data)
            })
            .catch((error) => {
                console.log(value);
                console.log(error);
                console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
            });
    },

    actionTests: ({commit}, data) => {
        commit('setTests', data);
    },
    actionSteps: ({commit}, data) => {
        commit('setSteps', data);
    },
    actionBugs: ({commit}, data) => {
        commit('setBugs', data);
    },
    actionModules: ({commit}, data) => {
        commit('setModules', data);
    },
};

const getters = {
    getTests: state => {
        return state.tests
    },

    getSteps: state => {
        return state.steps
    },

    getBugs: state => {
        // return state.bugs.filter(i => state.notRenderBugs.indexOf(i['status']) === -1)
        return state.bugs
    },

    getModules: state => {
        return state.modules
    },

    getNotRenderBugs: state => {
        return state.notRenderBugs
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
}