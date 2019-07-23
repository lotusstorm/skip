import { HTTP, distributor } from '../globalSettings'


const state = {
    data: [],
    issues: [],

    globalLoaderShow: false,
    addIssueLoaderShow: false,
    notRenderIssues: ['qa.Closed', 'dev.Closed', 'dev.Resolved', 'qa.Resolved']
};

const mutations = {
    setData: (state, data) => {
        state.data = data;
    },

    setIssues: (state, data) => {
        data.forEach(el => el['bind'] = false);
        state.issues = data.sort(i => i['id']).reverse()
    },

    setGlobalLoaderShow: (state, value) => {
        state.globalLoaderShow = value
    },

    setAddIssueLoaderShow: (state, value) => {
        state.addIssueLoaderShow = value
    },
};

const actions = {

    loadIssues: ({commit}) => {
        HTTP.get("/issues")
            .then((response) => {
                commit('setIssues', response.data.data);
            })
            .catch((error) => {
                console.log(error);
                console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
            })
    },

    loadData: ({commit}, data) => {
        commit('setGlobalLoaderShow', true);
        HTTP.post("/categories", {
                branch: data.branch,
                os: data.os
            })
            .then((response) => {
                let data = response.data.data;
                distributor(data);
                commit('setData', data);
            })
            .catch((error) => {
                console.log(error);
                console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
            }).finally(() => {
                commit('setGlobalLoaderShow', false);
            });
    },

    actionIssues: ({commit}, data) => {
        commit('setIssues', data);
    },

    loadGlobalLoaderShow: ({commit}, value) => {
        commit('setGlobalLoaderShow', value);
    },

    loadAddIssueLoaderShow: ({commit}, value) => {
        commit('setAddIssueLoaderShow', value);
    },
};

const getters = {
    getData: state => {
        return state.data
    },

    getIssues: state => {
        return state.issues
    },

    getGlobalLoaderShow: state => {
        return state.globalLoaderShow
    },

    getAddIssueLoaderShow: state => {
        return state.addIssueLoaderShow
    },

    getNotRenderIssues: state => {
        return state.notRenderIssues
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
}