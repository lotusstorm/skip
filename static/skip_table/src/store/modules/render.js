const state = {
    homeIssuesFilter: 'all',
    homeIssuesSearch: '',

    dataSearch: '',

    settingsIssuesSearch: '',

    selected: {
        id: null,
        status: false,
        data: [],
    },

    branch: 'an-minor',
    os: 'windows',
};

const mutations = {
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
        state.branch = value
    },

    setDataSearch: (state, value) => {
        state.dataSearch = value
    },

    setOs: (state, value) => {
        state.os = value.toLowerCase()
    },
};

const actions = {
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
        return state.branch
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