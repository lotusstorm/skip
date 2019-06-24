<template>
    <div class="app-content">
        <app-branches></app-branches>
        <div class="app_wrapper">
            <div class="table">
                <div class="table_wrapper">
                    <div class="title">
                        <h1 class="content">Modules</h1>
                    </div>
                    <div class="content-wrapper">
                        <app-parent-component
                                v-for="(category, key) in renderCategories"
                                :name="category"
                                :key="key"
                                :id="key"
                                :modifier="'category--style'"
                        >
                            <app-parent-component
                                v-for="(component, key) in renderComponents(getModules, category)"
                                :name="component"
                                :key="key"
                                :id="key"
                                :modifier="'component--style'"
                            >
                                <ul class="list">
                                    <app-module-item
                                            v-for="module in categoryComponentRender(getModules, category, component)"
                                            :key="module.id"
                                            :id="module.module_id"
                                            :name="module.name"
                                            :description="module.name"
                                            :data="getModules"
                                            :category="getModuleCategory"
                                    ></app-module-item>
                                </ul>
                            </app-parent-component>
                        </app-parent-component>
                    </div>
                </div>
                <app-search :searchAction="loadHomeModulesSearch" :getSearchValue="getHomeModulesSearch"></app-search>
            </div>
            <div class="table">
                <div class="table_wrapper">
                    <div class="title">
                        <h1 class="content">Tests</h1>
                    </div>
                    <ul class="list">
                        <app-custom-item
                                v-for="test in renderTests"
                                :key="test.id"
                                :id="test.test_id"
                                :checked="test.skip"
                                :name="test.name"
                                :description="test.name"
                                :data="renderTests"
                                :category="getTestCategory"
                        >
                            <app-custom-item
                                    v-for="step in renderStepsForTest(getSteps, test.test_id)"
                                    :key="step.id"
                                    :id="step.step_id"
                                    :checked="step.skip"
                                    :name="step.name"
                                    :description="step.description"
                                    :data="getSteps"
                                    :category="getStepCategory"
                            ></app-custom-item>
                        </app-custom-item>
                    </ul>
                </div>
                <!-- TODO убрать v-show="false" после отладки -->
<!--                v-show="false"-->
                <app-controllers-button
                        @event="updateTestsStepsModules"
                        :modifier="'update-tests-steps-modules'"
                        :description="'update-tests-steps-modules'"
                ></app-controllers-button>
            </div>
            <div class="table">
                <div class="table_wrapper">
                    <div class="title">
                        <h1 class="content">Issues</h1>
                    </div>
                    <app-filters :filterAction="loadHomeBugsFilter"></app-filters>
                    <ul class="list" v-show="getSelected.status">
                        <app-bug
                                class="item bug"
                                v-for="bug in renderBugs"
                                :key="bug.id"
                                :id="bug.id"
                                :checked="bug.bind"
                                :data="bug"
                        >
                        </app-bug>
                    </ul>
                </div>
                <app-search :searchAction="loadHomeBugsSearch" :getSearchValue="getHomeBugsSearch"></app-search>
            </div>
            <app-controllers></app-controllers>
        </div>
    </div>
</template>

<script>
    import Bug from '@/components/Bug.vue'
    import Search from '@/components/Search.vue'
    import Filters from '@/components/Filters.vue'
    import CustomItem from '@/components/CustomItem.vue'
    import ParentComponent from '@/components/ParentComponent.vue'
    import ModuleItem from '@/components/ModuleItem.vue'
    import ControllersButton from '@/components/ControllersButton.vue'
    import Controllers from '@/components/Controllers.vue'
    import Branches from '@/components/Branches.vue'
    import { mapActions, mapGetters } from 'vuex'
    import { HTTP } from '../store/globalSettings'


    export default {
        components: {
            'app-bug': Bug,
            'app-search': Search,
            'app-parent-component': ParentComponent,
            'app-custom-item': CustomItem,
            'app-module-item': ModuleItem,
            'app-filters': Filters,
            'app-controllers-button': ControllersButton,
            'app-controllers': Controllers,
            'app-branches': Branches,
        },
        computed: {
            ...mapGetters([
                'getTests',
                'getSteps',
                'getBugs',
                'getModules',
                'getTestCategory',
                'getStepCategory',
                'getBugCategory',
                'getModuleCategory',
                'getSelected',
                'getHomeBugsFilter',
                'getHomeTestsFilter',
                'getHomeBugsSearch',
                'getHomeTestsSearch',
                'getHomeModulesSearch',
                'getNotRenderBugs',
                'getBranch',
            ]),
            renderCategories() {
                let arr = this.getModules.map(i => i['categories']);
                return new Set(arr);
            },
            renderTests() {
                return this.getTests.filter(i => i['module_id'] === this.getModuleCategory['id'])
            },
            renderBugs() {
                if (this.getSelected['name'] === 'step') {
                    this.renderBugsCheckboxes(this.getSteps, this.getStepCategory, 'step_id');
                } else {
                    this.renderBugsCheckboxes(this.getTests, this.getTestCategory, 'test_id');
                }
                let data = this.getBugs.filter(i => this.getNotRenderBugs.indexOf(i['status']) === -1);
                return this.renderAfterFilter(data, this.getHomeBugsFilter, this.getHomeBugsSearch, 'bind');
                // return this.renderAfterFilter(this.getBugs, this.getHomeBugsFilter, this.getHomeBugsSearch, 'bind');
            }
        },
        methods: {
            ...mapActions([
                'loadHomeBugsFilter',
                'loadHomeTestsFilter',
                'loadHomeBugsSearch',
                'loadHomeTestsSearch',
                'loadHomeModulesSearch',
                'loadTestCategory',
                'loadStepCategory',
                'actionTests',
                'actionSteps',
                'actionModules',
            ]),
            updateTestsStepsModules() {
                let data = {
                        id: null,
                        status: false
                    };

                HTTP.put('/global_requests', {
                        branch: this.getBranch,
                        data
                    })
                    .then((response) => {
                        this.loadTestCategory(data);
                        this.loadStepCategory(data);
                        this.actionModules(response.data.modules);
                        this.actionTests(response.data.tests);
                        this.actionSteps(response.data.steps);
                        // console.log(response.data.tests);/
                        // console.log(response.data.steps);
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                    });
            },
            renderComponents(data, category) {
                let arr = data.map(i => i['categories'] === category ? i['components'] : []).filter(i => i.indexOf(this.getHomeModulesSearch) !== -1);
                return new Set(arr);
            },
            renderStepsForTest(data, test_id) {
                return data.filter(i => i['test_id'] === test_id);
            },
            categoryComponentRender(data, category, component) {
                return data.filter(i => i['categories'] === category && i['components'] === component);
            },
            renderBugsCheckboxes(data, category, key) {
                this.getBugs.forEach(el => el['bind'] = false);

                if (category['id'] != null) {
                    this.getBugs.forEach((bug) => {
                        data.find(i => i[key] === category['id'])['bugs']
                            .forEach(el => {
                                if (bug['id'] === el) bug['bind'] = true;
                            });
                    });
                }
            },
            renderAfterFilter(data, filter, search, key) {
                let arr;
                if (filter === 'checked') {
                    arr = data.filter(i => i[key]);
                } else if (filter === 'unchecked') {
                    arr = data.filter(i => !i[key]);
                } else {
                    arr = data;
                }
                return this.search(arr, search)
            },

            search(data, value) {
                return data.filter((el) => el['name'].toLowerCase().indexOf(value.toLowerCase()) !== -1)
            },
        },
    }
</script>
