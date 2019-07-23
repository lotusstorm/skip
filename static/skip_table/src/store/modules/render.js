const state = {
    homeIssuesFilter: 'all',
    homeIssuesSearch: '',

    dataSearch: '',

    settingsIssuesFilter: 'all',
    settingsIssuesSearch: '',

    selected: {
        id: null,
        status: false,
        name: 'category',
        data: [],
    },

    // ****************** FUTURE ***********************

    projects: ["ACR"],
    statuses: ["dev.Open"],

    // *************************************************

    testRender: {
        data: [],
        disable: false,
    },

    issueCategory: {
        name: 'Issue'
    },

    Branch: 'development',
    os: 'windows',
};

const mutations = {
    setTestRender: (state, data) => {
        state.testRender = data;
    },

    setSelected: (state, data) => {
        state.selected = data
    },

    setHomeIssuesFilter: (state, value) => {
        state.homeIssuesFilter = value;
    },

    setHomeModulesSearch: (state, value) => {
        state.homeModulesSearch = value;
    },

    setHomeIssuesSearch: (state, value) => {
        state.homeIssuesSearch = value;
    },

    setSettingsIssuesSearch: (state, value) => {
        state.settingsIssuesSearch = value;
    },

    setBranch: (state, value) => {
        state.Branch = value
    },

    setDataSearch: (state, value) => {
        state.dataSearch = value
    },

    setOs: (state, value) => {
        state.os = value.toLowerCase()
    },
};

const actions = {
    loadTestRender: ({commit}, data) => {
        commit('setTestRender', data);
    },

    loadSelected: ({commit}, data) => {
        commit('setSelected', data);
    },

    loadHomeIssuesFilter: ({commit}, value) => {
        commit('setHomeIssuesFilter', value);
    },

    loadHomeIssuesSearch: ({commit}, value) => {
        commit('setHomeIssuesSearch', value);
    },

    loadHomeModulesSearch: ({commit}, value) => {
        commit('setHomeModulesSearch', value);
    },

    loadSettingsIssuesSearch: ({commit}, value) => {
        commit('setSettingsIssuesSearch', value);
    },

    loadBranch: ({commit}, value) => {
        commit('setBranch', value);
    },

    loadDataSearch: ({commit}, value) => {
        commit('setDataSearch', value);
    },

    loadOs: ({commit}, value) => {
        commit('setOs', value);
    },
};

const getters = {
    getTestRender: state => {
        return state.testRender
    },

    getSelected: state => {
        return state.selected
    },

    getHomeIssuesFilter: state => {
        return state.homeIssuesFilter
    },

    getHomeIssuesSearch: state => {
        return state.homeIssuesSearch
    },

    getHomeModulesSearch: state => {
        return state.homeModulesSearch
    },

    getDataSearch: state => {
        return state.dataSearch
    },

    getSettingsIssuesSearch: state => {
        return state.settingsIssuesSearch
    },

    getBranch: state => {
        return state.Branch
    },

    getOs: state => {
        return state.os
    },
};

export default {
    state,
    getters,
    mutations,
    actions,
}