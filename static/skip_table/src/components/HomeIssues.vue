<template>
    <div class="table__wrapper">
        <app-filters :filterAction="loadHomeIssuesFilter"></app-filters>
        <ul :class="['table__content-list', {'disable' : !getSelected.status }]" id="issues" @scroll="onScroll">
            <app-issue
                    class="table__content-item"
                    v-for="issue in renderIssues"
                    :key="issue.id"
                    :id="issue.id"
                    :checked="issue.bind"
                    :data="issue"
                    :modifier="'issue--style'"
            >
            </app-issue>
        </ul>
        <app-search :searchAction="loadHomeIssuesSearch" :getSearchValue="getHomeIssuesSearch"></app-search>
    </div>
</template>

<script>
    import Issue from '@/components/Issue.vue'
    import Search from '@/components/Search.vue'
    import Filters from '@/components/Filters.vue'
    import { mapActions, mapGetters } from 'vuex'
    import { searchIssue, scroll } from '../store/globalSettings'


    export default {
        components: {
            'app-issue': Issue,
            'app-search': Search,
            'app-filters': Filters,
        },
        computed: {
            ...mapGetters([
                'getIssues',
                'getSelected',
                'getHomeIssuesFilter',
                'getHomeIssuesSearch',
                'getNotRenderIssues',
            ]),
            /**
             * Render функция для отрисовки issues в блоке Issues
             **/
            renderIssues() {
                this.renderIssuesCheckboxes(this.getSelected);

                let data = this.getIssues.filter(i => this.getNotRenderIssues.indexOf(i['status']) === -1);
                return this.renderAfterFilter(data, this.getHomeIssuesFilter, this.getHomeIssuesSearch);
                // return this.renderAfterFilter(this.getIssues, this.getHomeIssuesFilter, this.getHomeIssuesSearch, 'bind');
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
        },
    }
</script>