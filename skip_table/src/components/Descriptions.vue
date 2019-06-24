<template>
    <div class="description-wrapper">
        <div class="description-controls">
            <app-custom-button
                    :id="id"
                    :modifier="'single-update-button'"
                    @event="putBug(id)"
            ></app-custom-button>
            <app-custom-button
                    :id="id"
                    :modifier="'hide-description-button'"
                    @event="toItems"
            ></app-custom-button>
        </div>
        <div class="bug-description__wrapper">
            <h1 class="bug-summary"> {{ bug.summary }} </h1>
            <ul class="bug-description-container">
                <li class="bug-name description-row"> Name: {{ bug.name }} </li>
                <li class="bug-status description-row">
<!--                    <img  class="bug-status__img" :src="bug.statusImg" alt="">-->
                    <h1 class="bug-status__name ">{{ bug.statusName }} </h1>
                </li>
                <li class="bug-reporter description-row"> Reporter: {{ bug.reporter }} </li>
                <li class="bug-priority description-row">
                    <img class="bug-priority__img" :src="bug.priorityImg" alt="priority">
                    <h1 class="bug-priority__name "> {{ bug.priorityName }} </h1>
                </li>
            </ul>
            <div class="bug-description">
                <h1 class="bug-description__title">Description</h1>
                <p class="bug-description__content">{{ bug.description }}</p>
            </div>
        </div>
    </div>
</template>

<script>
    import CustomButton from '@/components/CustomButton.vue'
    import { HTTP } from '../store/globalSettings'
    import { mapGetters } from 'vuex'


    export default {
        data() {
            return {
                id: Number(this.$route.params.id),
                bug: []
            }
        },
        name: "Descriptions",
        components: {
            'app-custom-button': CustomButton,
        },
        beforeRouteEnter(to, from, next) {
            next(vm => {
                vm.getBug(vm.id);
            })
        },
        computed: {
            ...mapGetters([
                'getBugs',
            ]),
        },
        methods: {
            toItems() {
                this.$router.push({name: 'items'})
            },
            getBug(id) {
                HTTP.post('/bug', {
                        id
                    })
                    .then((response) => {
                        this.bug = response.data.data;
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                    });
            },
            updateBug(data) {
                let el = this.getBugs.find(i => i['id'] === data.id);

                el['name'] = data.name;
                el['status'] = data.status;
                el['description'] = data.description;
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
                    });
            },
        }
    }
</script>

<style scoped>
    .description-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        color: var(--bug-description-text-color);

    }

    .description-controls {
        display: flex;
        flex-flow: row wrap;
    }

    .bug-description-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        width: 80%;
        flex-grow: 1;
    }

    .bug-priority, .bug-status {
        display: flex;
        flex-flow: row;
    }

    .bug-priority__img {
        height: 20px;
    }

    .bug-description__wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    .bug-description {
        display: flex;
        width: 100%;
        flex-direction: column;
        align-items: center;
        margin: 5px 0;
        flex-grow: 2;
    }

    .bug-description__content {
        width: 98%;
        word-wrap: break-word;
        color: var(--bug-description-text-color);
        background-color: var(--bug-description-bg-color);
        padding: 10px 2px;
        overflow: auto;
    }

    .description-row {
        display: flex;
        align-items: center;
        padding: 5px;
        background-color: var(--bug-description-row-bg-color);
        border-radius: 3px;
        margin: 1px;
    }

    .bug-summary {
        color: var(--bug-description-title-text-color);
        margin: 1px;
        padding: 5px;
        font-size: 30px;
    }

    .bug-description__title {
        color: var(--bug-description-title-text-color);
        font-size: 20px;
        margin: 5px;
    }
</style>