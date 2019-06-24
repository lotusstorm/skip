<template>
    <div class="table_wrapper">
        <app-add-bug-panel @event="addBug"></app-add-bug-panel>
        <ul class="list">
            <app-settings-bug
                    class="item bug"
                    v-for="bug in renderSettingsBugs"
                    :key="bug.id"
                    :id="bug.id"
                    :data="bug"
                    :checked="bug.bind"
            >
                <template>
                    <app-custom-button
                            :id="bug.id"
                            :modifier="'single-update-button'"
                            @event="putBug(bug.id)"
                    ></app-custom-button>
                    <app-custom-button
                            :id="bug.id"
                            :modifier="'single-delete-button'"
                            @event="deleteBug(bug.id)"
                    ></app-custom-button>
                    <app-custom-button
                            :id="bug.id"
                            :modifier="'show-description-button'"
                            @event="toDescriptions(bug.id)"
                    ></app-custom-button>
                </template>
            </app-settings-bug>
        </ul>
            <router-view/>
            <app-db-controllers>
                <template>
                    <app-controllers-button
                            :disabled="getBugs.length === 0"
                            @event="deleteAllBugs"
                            :modifier="'delete-all'"
                            :description="'DeleteAll'"
                    ></app-controllers-button>
                    <app-controllers-button
                            :disabled="getBugs.length === 0"
                            @event="updateAllBugs"
                            :modifier="'update-all'"
                            :description="'UpdateAll'"
                    ></app-controllers-button>
                </template>
            </app-db-controllers>
            <app-search :searchAction="loadSettingsBugsSearch"></app-search>
    </div>
</template>

<script>
    import SettingsBug from '@/components/SettingsBug.vue'
    import CustomButton from '@/components/CustomButton.vue'
    import AddBugPanel from '@/components/AddBugPanel.vue'
    import Search from '@/components/Search.vue'
    import DbControllers from '@/components/DbControllers.vue'
    import ControllersButton from '@/components/ControllersButton.vue'
    import { mapGetters, mapActions } from 'vuex'
    import { HTTP } from '../store/globalSettings'

    export default {
        components: {
            'app-search': Search,
            'app-add-bug-panel': AddBugPanel,
            'app-db-controllers': DbControllers,
            'app-controllers-button': ControllersButton,
            'app-settings-bug': SettingsBug,
            'app-custom-button': CustomButton,
        },
        computed: {
            ...mapGetters([
                'getBugs',
                'getTests',
                'getSteps',
                'getSettingsBugsFilter',
                'getSettingsBugsSearch',
                'getNotRenderBugs',
                'getBranch',
            ]),

            renderSettingsBugs() {
                return this.search(this.getBugs, this.getSettingsBugsSearch)
            },
        },
        methods: {
            ...mapActions([
                'loadSettingsBugsFilter',
                'loadSettingsBugsSearch',
                'actionBugs',
                'actionTests',
                'actionSteps',
                'loadTests',
                'loadSteps',
                'loadSelected',
            ]),

            search(data, value) {
                return data.filter((el) => el['name'].toLowerCase().indexOf(value.toLowerCase()) !== -1)
            },

            updateBug(data) {
                let el = this.getBugs.find(i => i['id'] === data.id);

                el['name'] = data.name;
                el['status'] = data.status;
                el['description'] = data.description;

                this.loadTests(this.getBranch);
                this.loadSteps(this.getBranch);
            },

            delBug(data) {
                this.getBugs.forEach((el, index) => {
                    if (el['id'] === data.id) {
                        this.getBugs.splice(index, 1);
                    }
                });
            },

            putBug(id) {
                HTTP.put('/bug/update', {
                        id
                    })
                    .then((response) => {
                        const data = response.data.data;
                        this.updateBug(data);
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                        alert(`${error.response.data.status}`);
                    });
            },

            toDescriptions(id) {
                this.$router.push({ name: 'description', params: { id } })
            },

            deleteBug(id) {
                /**
                 *
                 */
                if (confirm('элемент будет !!! УДАЛЕН !!! из базы данных, вы согласны ??')) {
                    HTTP.post('/bug/delete', {
                        id
                    })
                        .then((response) => {
                            const data = response.data.data;

                            this.delBug(data);
                            this.loadTests(this.getBranch);
                            this.loadSteps(this.getBranch);

                        })
                        .catch((error) => {
                            console.log(error);
                            console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                            alert(`${error.response.data.status}`);
                        });
                }
            },
            updateAllBugs() {
                /**
                 *
                 */
                HTTP.put('/bugs', {
                        issues: this.getBugs.map(i => i['name'])
                    })
                    .then((response) => {
                        const data = response.data.data;
                        this.actionBugs(data);
                        this.loadTests(this.getBranch);
                        this.loadSteps(this.getBranch);
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                        alert(`${error.response.data.status}`);
                    });
            },

            deleteAllBugs() {
                if (confirm('база данных багов будет !!! ОЧИЩЕННА !!!, вы согласны ??')) {
                    HTTP.delete('/bugs')
                    .then((response) => {
                        const data = response.data.data;

                        this.actionBugs(data);
                        this.loadTests(this.getBranch);
                        this.loadSteps(this.getBranch);
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                        alert(`${error.response.data.status}`);
                    });
                }
            },
            addBug(event, value) {
                HTTP.post('/bug/add', {
                        key: value
                    })
                    .then((response) => {
                        const data = response.data.data;
                        data.forEach(el => {
                            this.getBugs.push(el);
                        });
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                        alert(`${error.response.data.status}`);
                    });
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
