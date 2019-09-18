<template>
    <div class="description-wrapper">
        <div class="description-controls">
            <app-custom-button
                    :id="id"
                    :modifier="'single-update-button'"
                    @event="putIssue(id)"
            ></app-custom-button>
            <app-custom-button
                    :id="id"
                    :modifier="'hide-description-button'"
                    @event="toItems"
            ></app-custom-button>
        </div>
        <div class="issue-description__wrapper">
            <h1 class="issue-summary"> {{ issue.summary }} </h1>
            <ul class="issue-description-container">
                <li class="issue-name description-row"> Name: {{ issue.name }} </li>
                <li class="issue-status description-row">
                    <h1 class="issue-status__name ">{{ issue.statusName }} </h1>
                </li>
                <li class="issue-reporter description-row"> Reporter: {{ issue.reporter }} </li>
                <li class="issue-priority description-row">
                    <img class="issue-priority__img" :src="issue.priorityImg" alt="priority">
                    <h1 class="issue-priority__name "> {{ issue.priorityName }} </h1>
                </li>
            </ul>
            <div class="issue-description">
                <h1 class="issue-description__title">Description</h1>
                <p class="issue-description__content">{{ issue.description }}</p>
            </div>
        </div>
    </div>
</template>

<script>
    import CustomButton from '@/components/CustomButton.vue'
    import { HTTP, updater } from '../store/globalSettings'
    import { mapGetters, mapActions } from 'vuex'


    export default {
        name: "Descriptions",
        data() {
            return {
                id: Number(this.$route.params.id),
                issue: []
            }
        },
        components: {
            'app-custom-button': CustomButton,
        },
        beforeRouteEnter(to, from, next) {
            next(vm => {
                vm.getIssue(vm.id);
            })
        },
        computed: {
            ...mapGetters([
                'getIssues',
                'getNotRenderIssues',
            ]),
        },
        methods: {
            ...mapActions([
                'loadGlobalLoaderShow',
            ]),
            /**
             * роутинг
             */
            toItems() {
                // this.$router.push({name: 'items'});
                this.$router.go(-1);
            },
            /**
             * Метод для получения развернутой информации об issue по id
             * @param id
             */
            getIssue(id) {
                this.loadGlobalLoaderShow(true);
                HTTP.post('/issue', {
                        id
                    })
                    .then((response) => {
                        this.issue = response.data.data;
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                    })
                    .finally(() => this.loadGlobalLoaderShow(false));
            },
            /**
             * Метод для обновления issue на клиенте
             * @param data
             */
            updateIssue(data) {
                let el = this.getIssues.find(i => i['id'] === data.id);

                el['name'] = data.name;
                el['status'] = data.status;
                el['summary'] = data.summary;

                if (this.getNotRenderIssues.indexOf(el['status']) !== -1) {
                    updater(this.getData,  data.id);
                }
            },
            /**
             * Метод для обновления issue в БД
             * @param id
             */
            putIssue(id) {
                this.loadGlobalLoaderShow(true);
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
                    .finally(() => this.loadGlobalLoaderShow(false));
            },
        }
    }
</script>

<style scoped>
    .description-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        color: var(--issue-summary-text-color);
        overflow: auto;
    }

    .description-controls {
        display: flex;
        flex-flow: row wrap;
    }

    .issue-description-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        width: 80%;
        flex-grow: 1;
    }

    .issue-priority, .issue-status {
        display: flex;
        flex-flow: row;
    }

    .issue-priority__img {
        height: 20px;
    }

    .issue-description__wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    .issue-description {
        display: flex;
        width: 100%;
        flex-direction: column;
        align-items: center;
        margin: 5px 0;
        flex-grow: 2;
    }

    .issue-description__content {
        width: 98%;
        word-wrap: break-word;
        color: var(--issue-summary-text-color);
        background-color: var(--issue-summary-bg-color);
        padding: 10px 2px;
    }

    .description-row {
        display: flex;
        align-items: center;
        padding: 5px;
        background-color: var(--issue-summary-row-bg-color);
        border-radius: 3px;
        margin: 1px;
    }

    .issue-summary {
        color: var(--issue-summary-title-text-color);
        margin: 1px;
        padding: 5px;
        font-size: 30px;
    }

    .issue-description__title {
        color: var(--issue-summary-title-text-color);
        font-size: 20px;
        margin: 5px;
    }
</style>