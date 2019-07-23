<template>
    <div class="app-content">
        <app-branches></app-branches>
        <div class="main-content">
            <div class="app-wrapper">
                <div class="table">
                    <div class="table__wrapper">
                        <div class="table__title">
                            <h1 class="table__title-content">Modules</h1>
                        </div>
                        <div class="table__content-wrapper">
                            <ul class="table__content-list">
                                <app-custom-item
                                        v-for="category in renderCategories"
                                        :key="category.id"
                                        :id="category.category_id"
                                        :data="category"
                                        :description="category.name"
                                        :category="'category'"
                                        :modifier="'category--style'"
                                        :active="'modules--active'"
                                >
                                    <app-custom-item
                                            v-for="component in category.components"
                                            :key="component.id"
                                            :id="component.component_id"
                                            :data="component"
                                            :description="category.name"
                                            :category="'component'"
                                            :modifier="'component--style'"
                                            :active="'modules--active'"
                                    >
                                        <app-custom-item
                                                v-for="module in component.modules"
                                                :key="module.id"
                                                :id="module.module_id"
                                                :data="module"
                                                :description="component.name"
                                                :category="'module'"
                                                :modifier="'module--style'"
                                                :active="'modules--active'"
                                        ></app-custom-item>
                                    </app-custom-item>
                                </app-custom-item>
                            </ul>
                        </div>
                    </div>
<!--                    <app-search :searchAction="loadDataSearch" :getSearchValue="getDataSearch"></app-search>-->
                </div>
                <div class="table">
                    <div class="table__wrapper">
                        <div class="table__title">
                            <h1 class="table__title-content">Tests</h1>
                        </div>
                        <ul :class="['table__content-list', {'disable' : !getTestRender.disable}]">
                            <app-custom-item
                                    v-for="test in getTestRender.data"
                                    :key="test.id"
                                    :id="test.test_id"
                                    :description="test.name"
                                    :data="test"
                                    :category="'test'"
                                    :modifier="'test--style'"
                                    :active="'tests--active'"
                            >
                                <app-custom-item
                                        v-for="step in test.steps"
                                        :key="step.id"
                                        :id="step.step_id"
                                        :description="step.description"
                                        :data="step"
                                        :category="'step'"
                                        :modifier="'step--style'"
                                        :active="'tests--active'"
                                ></app-custom-item>
                            </app-custom-item>
                        </ul>
                    </div>
                    <!-- TODO убрать v-show="false" после отладки -->
    <!--                -->
    <!--                <app-controllers-button-->
    <!--                        v-show="false"-->
    <!--                        @event="updateTestsStepsModules"-->
    <!--                        :modifier="'update-tests-steps-modules'"-->
    <!--                        :description="'update-tests-steps-modules'"-->
    <!--                ></app-controllers-button>-->
                </div>
                <div class="table">
                    <div class="table__wrapper">
                        <div class="table__title">
                            <h1 class="table__title-content">Issues</h1>
                        </div>
                        <app-filters :filterAction="loadHomeIssuesFilter"></app-filters>
                        <ul :class="['table__content-list', {'disable' : !getSelected.status }]">
                            <app-issue
                                    class="table__content-item issue"
                                    v-for="issue in renderIssues"
                                    :key="issue.id"
                                    :id="issue.id"
                                    :checked="issue.bind"
                                    :data="issue"
                                    :modifier="'issue--style'"
                            >
                            </app-issue>
                        </ul>
                    </div>
                    <app-search :searchAction="loadHomeIssuesSearch" :getSearchValue="getHomeIssuesSearch"></app-search>
                </div>
            </div>
            <app-controllers></app-controllers>
        </div>
    </div>
</template>

<script>
    import Issue from '@/components/Issue.vue'
    import Search from '@/components/Search.vue'
    import Filters from '@/components/Filters.vue'
    import CustomItem from '@/components/CustomItem.vue'
    import Controllers from '@/components/Controllers.vue'
    import Branches from '@/components/Branches.vue'
    import { mapActions, mapGetters } from 'vuex'
    import { searchIssue } from '../store/globalSettings'


    export default {
        components: {
            'app-issue': Issue,
            'app-search': Search,
            'app-custom-item': CustomItem,
            'app-filters': Filters,
            'app-controllers': Controllers,
            'app-branches': Branches,
        },
        computed: {
            ...mapGetters([
                'getData',
                'getIssues',
                'getSelected',
                'getHomeIssuesFilter',
                'getHomeIssuesSearch',
                'getHomeModulesSearch',
                'getNotRenderIssues',
                'getBranch',
                'getTestRender',
                'getDataSearch',
                'getDataForRender',
            ]),
            /**
             * Render функция для отрисовки дерева в блоке Modules
             **/
            renderCategories() {
                // this.searchInTree(this.getData, this.getDataSearch);
                // return this.getDataForRender;
                return this.getData;
            },
            /**
             * Render функция для отрисовки issues в блоке Issues
             **/
            renderIssues() {
                this.renderIssuesCheckboxes(this.getSelected);
                let data = this.getIssues.filter(i => this.getNotRenderIssues.indexOf(i['status']) === -1);
                return this.renderAfterFilter(data, this.getHomeIssuesFilter, this.getHomeIssuesSearch);
                // return this.renderAfterFilter(this.getIssues, this.getHomeIssuesFilter, this.getHomeIssuesSearch, 'bind');
            }
        },
        methods: {
            ...mapActions([
                'loadHomeIssuesFilter',
                'loadHomeIssuesSearch',
                'loadHomeModulesSearch',
                'loadGlobalLoaderShow',
                'loadTestRender',
                'loadDataSearch',
            ]),
            // updateTestsStepsModules() {
            //     let data = {
            //         id: null,
            //         status: false
            //     };
            //     this.loadGlobalLoaderShow(true);
            //     HTTP.put('/global_requests', {
            //             branch: this.getBranch,
            //             data
            //         })
            //         .then((response) => {
            //             // IMPORTANT переделать
            //             // this.loadTestCategory(data);
            //             // this.loadStepCategory(data);
            //             // this.actionModules(response.data.modules);
            //             // this.actionTests(response.data.tests);
            //             // this.actionSteps(response.data.steps);
            //         })
            //         .catch((error) => {
            //             console.log(error);
            //             console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
            //         })
            //         .finally(() => this.loadGlobalLoaderShow(false));
            // },
            /**
             * Проставляет галочки на привязанных элементах выбранного объекта
             * @param { Object } data - выбранный объект
             */
            renderIssuesCheckboxes(data) {
                this.getIssues.forEach(el => el['bind'] = false);
                if (data['data'] !== undefined && data['data'].length !== 0) {
                    this.getIssues.forEach(issue => {
                        data['data']['issues'].forEach(el => {
                            if (issue['id'] === el) issue['bind'] = true;
                        });
                    });
                }
            },
            /**
             * Отфильтровывает issues не подходящие критериям
             * @param data массив issues
             * @param filter (check, uncheck, all)
             * @param search критерии поиска
             */
            renderAfterFilter(data, filter, search) {
                let arr;
                if (filter === 'checked') {
                    arr = data.filter(i => i['bind']);
                } else if (filter === 'unchecked') {
                    arr = data.filter(i => !i['bind']);
                } else {
                    arr = data;
                }
                return searchIssue(arr, search)
            },
            // /**
            // IMPORTANT допилить поиск по тестам
            //  * Поиск нужного елемента в дерева объектов Modules
            //  * @param {Array} data - массив в котором производится поиск (неизменняемый)
            //  * @param {Array} render - масив который отрисовывается (изменяемый)
            //  * @param {String} value - искомое значение
            //  */
            // searchInTree(data, render, value) {
            //     data = Array.isArray(data) ? data : [data];
            //
            //     data.forEach((el, i) => {
            //         render[i]['components'] = el['components'].filter(j => j['name'].indexOf(value) !== -1);
            //     });
            // },
            // searchInTree(event) {
            //     console.log(event.target.value);
            //     let data = Array.isArray(this.getData) ? this.getData : [this.getData];
            //     let render = data.map(a => ({...a}));
            //
            //     data.forEach(el => {
            //         let componentId = el['components'].find(j => j['name'].indexOf(this.getDataSearch) === -1)['component_id'];
            //         let element = document.getElementById(`${componentId}`);
            //         element.classList.add('display');
            //     });
            // },
        },
    }
</script>

<style>
    .display {
        display: none;
    }
</style>