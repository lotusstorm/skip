const state = {
    globalLoaderShow: false,

    homeTestsFilter: 'all',
    homeTestsSearch: '',

    homeBugsFilter: 'all',
    homeBugsSearch: '',

    homeModulesFilter: 'all',
    homeModulesSearch: '',

    settingsBugsFilter: 'all',
    settingsBugsSearch: '',

    selected: {
        id: null,
        status: false,
        name: 'test'
    },

    projects: ["ACR"],
    statuses: ["dev.Open"],

    testCategory: {
        id: null,
        status: false,
        name: 'test'
    },
    stepCategory: {
        id: null,
        status: false,
        name: 'step'
    },
    moduleCategory: {
        id: null,
        name: 'module'
    },

    bugCategory: {
        name: 'bug'
    },

    Branch: 'development',
};

const mutations = {
    setSettingsBugRender: (state, bugs) => {
        state.bugs = bugs.sort(i => i['id']).reverse()
    },

    setGlobalLoaderShow: (state, value) => {
        state.globalLoaderShow = value
    },

    setTestCategory: (state, data) => {
        state.testCategory.id = data.id;
        state.testCategory.status = data.status;
    },

    setModuleCategory: (state, data) => {
        state.moduleCategory.id = data.id;
    },

    setStepCategory: (state, data) => {
        state.stepCategory.id = data.id;
        state.stepCategory.status = data.status;
    },

    setSelected: (state, data) => {
        state.selected = data
    },

    setHomeBugsFilter: (state, value) => {
        state.homeBugsFilter = value;
    },

    setHomeTestsFilter: (state, value) => {
        state.homeTestsFilter = value;
    },

    setHomeModulesFilter: (state, value) => {
        state.homeModulesFilter = value;
    },

    setHomeModulesSearch: (state, value) => {
        state.homeModulesSearch = value;
    },

    setSettingsBugsFilter: (state, value) => {
        state.settingsBugsFilter = value;
    },

    setHomeTestsSearch: (state, value) => {
        state.homeTestsSearch = value;
    },

    setHomeBugsSearch: (state, value) => {
        state.homeBugsSearch = value;
    },

    setSettingsBugsSearch: (state, value) => {
        state.settingsBugsSearch = value;
    },

    setBranch: (state, value) => {
        state.Branch = value
    },

};

const actions = {
    loadTestCategory: ({commit}, data) => {
        commit('setTestCategory', data);
    },

    loadGlobalLoaderShow: ({commit}, value) => {
        commit('setGlobalLoaderShow', value);
    },

    loadStepCategory: ({commit}, data) => {
        commit('setStepCategory', data);
    },

    loadModuleCategory: ({commit}, data) => {
        commit('setModuleCategory', data);
    },

    loadSelected: ({commit}, data) => {
        commit('setSelected', data);
    },

    loadHomeBugsFilter: ({commit}, value) => {
        commit('setHomeBugsFilter', value);
    },

    loadHomeTestsFilter: ({commit}, value) => {
        commit('setHomeTestsFilter', value);
    },

    loadHomeModulesFilter: ({commit}, value) => {
        commit('setHomeModulesFilter', value);
    },

    loadSettingsBugsFilter: ({commit}, value) => {
        commit('setSettingsBugsFilter', value);
    },

    loadHomeTestsSearch: ({commit}, value) => {
        commit('setHomeTestsSearch', value);
    },

    loadHomeBugsSearch: ({commit}, value) => {
        commit('setHomeBugsSearch', value);
    },

    loadHomeModulesSearch: ({commit}, value) => {
        commit('setHomeModulesSearch', value);
    },

    loadSettingsBugsSearch: ({commit}, value) => {
        commit('setSettingsBugsSearch', value);
    },

    loadBranch: ({commit}, value) => {
        commit('setBranch', value);
    },
};

const getters = {
    getTestCategory: state => {
        return state.testCategory
    },

    getGlobalLoaderShow: state => {
        return state.globalLoaderShow
    },

    getStepCategory: state => {
        return state.stepCategory
    },

    getBugCategory: state => {
        return state.bugCategory
    },

    getModuleCategory: state => {
        return state.moduleCategory
    },

    getSelected: state => {
        return state.selected
    },

    getHomeTestsFilter: state => {
        return state.homeTestsFilter
    },

    getHomeBugsFilter: state => {
        return state.homeBugsFilter
    },

    getHomeModulesFilter: state => {
        return state.homeModulesFilter
    },

    getSettingsBugsFilter: state => {
        return state.settingsBugsFilter
    },

    getHomeTestsSearch: state => {
        return state.homeTestsSearch
    },

    getHomeBugsSearch: state => {
        return state.homeBugsSearch
    },

    getHomeModulesSearch: state => {
        return state.homeModulesSearch
    },

    getSettingsBugsSearch: state => {
        return state.settingsBugsSearch
    },

    getBranch: state => {
        return state.Branch
    },
};

export default {
    state,
    getters,
    mutations,
    actions,
}