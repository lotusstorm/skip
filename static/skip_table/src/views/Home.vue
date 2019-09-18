<template>
    <div class="app-content">
        <app-branches></app-branches>
        <div class="main-content">
            <div class="app-wrapper">
                <div class="table modules">
                    <div class="table__title">
                        <h1 class="table__title-content">Modules</h1>
                    </div>
                    <div class="table__wrapper">
                        <div class="table__content-wrapper">
                            <ul class="table__content-list" id="modules" @scroll="onScroll">
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
                                            v-for="component in searchInTree(category.components, getDataSearch)"
                                            :key="component.id"
                                            :id="component.component_id"
                                            :data="component"
                                            :description="component.name"
                                            :category="'component'"
                                            :modifier="'component--style'"
                                            :active="'modules--active'"
                                    >
                                        <app-custom-item
                                                v-for="module in component.modules"
                                                :key="module.id"
                                                :id="module.module_id"
                                                :data="module"
                                                :description="module.name"
                                                :category="'module'"
                                                :modifier="'module--style'"
                                                :active="'modules--active'"
                                        ></app-custom-item>
                                    </app-custom-item>
                                </app-custom-item>
                            </ul>
                        </div>
                        <app-search :searchAction="loadDataSearch" :getSearchValue="getDataSearch"></app-search>
                    </div>
                </div>
                <div class="table tests">
                    <div class="table__title">
                        <h1 class="table__title-content">Tests</h1>
                    </div>
                    <div class="table__wrapper">
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
                </div>
                <div class="table issue">
                    <div class="table__title">
                        <h1 class="table__title-content">Issues</h1>
                    </div>
                    <router-view/>
                </div>
            </div>
            <app-controllers></app-controllers>
        </div>
    </div>
</template>

<script>
    import Search from '@/components/Search.vue'
    import CustomItem from '@/components/CustomItem.vue'
    import Controllers from '@/components/Controllers.vue'
    import Branches from '@/components/Branches.vue'
    import { mapActions, mapGetters } from 'vuex'
    import { scroll } from '../store/globalSettings'


    export default {
        components: {
            'app-search': Search,
            'app-custom-item': CustomItem,
            'app-controllers': Controllers,
            'app-branches': Branches,
        },
        computed: {
            ...mapGetters([
                'getData',
                'getTestRender',
                'getDataSearch',
            ]),
            /**
             * Render функция для отрисовки дерева в блоке Modules
             **/
            renderCategories() {
                return this.getData;
            },
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
            onScroll(event) { scroll(event); },
            /**
            IMPORTANT допилить поиск по тестам
             * Поиск нужного елемента в дерева объектов Modules
             * @param {Array} data - массив в котором производится поиск (неизменняемый)
             * @param {Array} render - масив который отрисовывается (изменяемый)
             * @param {String} value - искомое значение
             */
            searchInTree(data, value) {
                data = Array.isArray(data) ? data : [data];
                return data.filter(j => j['name'].indexOf(value) !== -1);
            },
        },
    }
</script>

<style>
    .display {
        display: none;
    }
</style>