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
                                        v-for="(item, index) in renderCategories"
                                        :key="index"
                                        :data="item"
                                        :category="'category'"
                                        :description="item.description ? item.description : item.name"
                                        :modifier="'category--style'"
                                        :active="'item--active'"
                                ></app-custom-item>
                            </ul>
                        </div>
<!--                        <app-search :searchAction="loadDataSearch" :getSearchValue="getDataSearch"></app-search>-->
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
    // import Search from '@/components/Search.vue'
    import CustomItem from '@/components/CustomItem.vue'
    import Controllers from '@/components/Controllers.vue'
    import Branches from '@/components/Branches.vue'
    import { mapActions, mapGetters } from 'vuex'
    import { scroll } from '../store/globalSettings'


    export default {
        components: {
            // 'app-search': Search,
            'app-custom-item': CustomItem,
            'app-controllers': Controllers,
            'app-branches': Branches,
        },
        computed: {
            ...mapGetters([
                'getData',
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
             * @param {String} value - искомое значение
             */
            // searchInTree(data, value) {
            //     data = Array.isArray(data) ? data : [data];
            //     return data.filter(j => j['name'].indexOf(value) !== -1);
            // },
        }
    }
</script>

<style>
    .display {
        display: none;
    }
</style>