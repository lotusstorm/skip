<template>
    <div class="table__wrapper">
        <app-add-bug-panel
                @event="addIssue"
                :show="getAddIssueLoaderShow"
                :modifier="'add-panel-button'"
        ></app-add-bug-panel>
        <ul class="table__content-list">
            <app-settings-issue
                    class="table__content-item issue"
                    v-for="issue in renderSettingsIssues"
                    :key="issue.id"
                    :id="issue.id"
                    :data="issue"
                    :checked="issue.bind"
                    :modifier="'issue--style'"
                    @event="toDescriptions(issue.id)"
            >
                <template>
                    <app-custom-button
                            :id="issue.id"
                            :modifier="'single-update-button'"
                            @event="putIssue(issue.id)"
                    ></app-custom-button>
                    <app-custom-button
                            :id="issue.id"
                            :modifier="'single-delete-button'"
                            @event="deleteIssue(issue.id)"
                    ></app-custom-button>
                </template>
            </app-settings-issue>
        </ul>
            <router-view/>
            <app-db-controllers>
                <template>
                    <app-controllers-button
                            :disabled="getIssues.length === 0"
                            @event="deleteAllIssues"
                            :modifier="'delete-all'"
                            :description="'DeleteAll'"
                    ></app-controllers-button>
                    <app-controllers-button
                            :disabled="getIssues.length === 0"
                            @event="updateAllIssues"
                            :modifier="'update-all'"
                            :description="'UpdateAll'"
                    ></app-controllers-button>
                </template>
            </app-db-controllers>
            <app-search :searchAction="loadSettingsIssuesSearch" :getSearchValue="getSettingsIssuesSearch"></app-search>
    </div>
</template>

<script>
    import SettingsBug from '@/components/IssueSettings.vue'
    import CustomButton from '@/components/CustomButton.vue'
    import AddBugPanel from '@/components/AddIssuePanel.vue'
    import Search from '@/components/Search.vue'
    import DbControllers from '@/components/DbControllers.vue'
    import ControllersButton from '@/components/ControllersButton.vue'
    import { mapGetters, mapActions } from 'vuex'
    import { HTTP, updater, searchIssue, status } from '../store/globalSettings'

    export default {
        components: {
            'app-search': Search,
            'app-add-bug-panel': AddBugPanel,
            'app-db-controllers': DbControllers,
            'app-controllers-button': ControllersButton,
            'app-settings-issue': SettingsBug,
            'app-custom-button': CustomButton,
        },
        computed: {
            ...mapGetters([
                'getIssues',
                'getSettingsIssuesSearch',
                'getAddIssueLoaderShow',
                'getNotRenderIssues',
                'getData',
                'getBranch',
                'getOs',
                'getSelected',
            ]),

            renderSettingsIssues() {
                return searchIssue(this.getIssues, this.getSettingsIssuesSearch)
            },
        },
        methods: {
            ...mapActions([
                'loadSettingsIssuesSearch',
                'actionIssues',
                'loadSelected',
                'loadGlobalLoaderShow',
                'loadAddIssueLoaderShow',
                'loadData'
            ]),
            /**
             * роутинг
             */
            toDescriptions(id) {
                this.$router.push({ name: 'description', params: { id } })
            },
            /**
             * Делает елемент не активным или активным
             */
            enableOrDisable(id, flag) {
                let element = document.getElementById(`${id}`);

                if (flag === 'disable') {
                    element.classList.add('disable');
                } else {
                    element.classList.remove('disable');
                }

            },
            /**
             * Метод для обновления issue на клиенте
             */
            updateIssue(data) {
                let el = this.getIssues.find(i => i['id'] === data.id);

                el['name'] = data.name;
                el['status'] = data.status;
                el['summary'] = data.summary;

                if (this.getNotRenderIssues.indexOf(el['status']) !== -1) {
                    updater(this.getData, data.id);
                    status(this.getData);
                }
            },
            /**
             * Метод для удаления issue на клиенте
             */
            delIssue(data) {
                this.getIssues.forEach((el, index) => {
                    if (el['id'] === data.id) {
                        this.getIssues.splice(index, 1);
                    }
                });

                updater(this.getData, data.id);
                status(this.getData);
            },
            /**
             * Метод для обновления issue в БД
             */
            putIssue(id) {
                this.enableOrDisable(id, 'disable');
                HTTP.put('/issue/update', {
                        id
                    })
                    .then((response) => {
                        const data = response.data.data;
                        this.updateIssue(data);
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                        alert(`${error.response.data.status}`);
                    })
                    .finally(() => this.enableOrDisable(id, 'enable'));
            },
            /**
             * Метод для удаления issue из БД
             */
            deleteIssue(id) {
                if (confirm('элемент будет !!! УДАЛЕН !!! из базы данных, вы согласны ??')) {
                    this.enableOrDisable(id, 'disable');
                    HTTP.post('/issue/delete', {
                            id
                        })
                        .then((response) => {
                            const data = response.data.data;
                            this.delIssue(data);
                        })
                        .catch((error) => {
                            console.log(error);
                            console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                            alert(`${error.response.data.status}`);
                            this.enableOrDisable(id, 'enable');
                        })
                }
            },
            /**
             * Метод для обновления всех issues в БД
             */
            updateAllIssues() {
                let data = {
                    branch: this.getBranch,
                    os: this.getOs
                };

                this.loadGlobalLoaderShow(true);
                HTTP.put('/issues', {
                        issues: this.getIssues.map(i => i['name'])
                    })
                    .then((response) => {
                        const issues = response.data.data;
                        this.actionIssues(issues);
                        this.loadData({'data': data, 'old_data': this.getData, 'cache': true});
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                        alert(`${error.response.data.status}`);
                    })
                    .finally(() => this.loadGlobalLoaderShow(false));
            },
            /**
             * Метод для уадаления всех issues из БД
             */
            deleteAllIssues() {
                if (confirm('база данных багов будет !!! ОЧИЩЕННА !!!, вы согласны ??')) {
                    let data = {
                        branch: this.getBranch,
                        os: this.getOs
                    };

                    this.loadGlobalLoaderShow(true);
                    HTTP.delete('/issues')
                        .then((response) => {
                            const issues = response.data.data;
                            this.actionIssues(issues);
                            this.loadData({'data': data, 'old_data': this.getData, 'cache': true});
                        })
                        .catch((error) => {
                            console.log(error);
                            console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                            alert(`${error.response.data.status}`);
                        })
                        .finally(() => this.loadGlobalLoaderShow(false));
                }
            },
            /**
             * Метод для добавления issue в БД
             * @param event - евент мыши
             * @param value - значение
             */
            addIssue(event, value) {
                this.loadAddIssueLoaderShow(true);
                HTTP.post('/issue/add', {
                        key: value
                    })
                    .then((response) => {
                        const data = response.data.data;
                        data.forEach(el => {
                            this.getIssues.push(el);
                        });
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                        alert(`${error.response.data.status}`);
                    })
                    .finally(() => this.loadAddIssueLoaderShow(false));
            }
        }
    }
</script>

<style scoped>
    .controllers-button {
        height: 40px;
        flex-grow: 1;
        background-color: #bd2f2f;
    }
</style>
