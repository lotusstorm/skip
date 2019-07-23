<template>
    <div class="controllers">
        <app-controllers-button
                :disabled="getData.length === 0"
                @event="save"
                :modifier="'save'"
                :description="'Save'"
        ></app-controllers-button>
        <app-controllers-button
                :disabled="getData.length === 0"
                @event="cancel"
                :modifier="'cancel'"
                :description="'Cancel'"
        ></app-controllers-button>
    </div>
</template>

<script>
    import { HTTP } from '../store/globalSettings'
    import { mapActions, mapGetters } from 'vuex'
    import ControllersButton from '@/components/ControllersButton.vue'


    export default {
        name: "Controllers",
        data() {
            return {
                store: []
            }
        },
        computed: {
            ...mapGetters([
                'getData',
                'getBranch',
                'getSelected',
                'getOs',
                'getDataForRender',
            ]),
        },
        components: {
            'app-controllers-button': ControllersButton,
        },
        methods: {
            ...mapActions([
                'loadGlobalLoaderShow',
                'loadData',
                'loadTestRender',
                'loadSelected',
            ]),
            /**
             * Сохраняет изменения на клиенте в БД
             */
            save() {
                // console.log(this.getData);
                // console.log(this.getDataForRender);
                this.loadGlobalLoaderShow(true);
                HTTP.put('/global_update', {
                        branch: this.getBranch,
                        data: this.getData,
                        os: this.getOs,
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                    })
                    .finally(() => this.loadGlobalLoaderShow(false));
            },
            /**
             * Откатывает все изменения на клиенте
             */
            cancel() {
                let render = {
                    data: [],
                };

                let data = {
                    branch: this.getBranch,
                    os: this.getOs
                };

                this.loadData(data);
                this.loadTestRender(render);
                this.loadSelected(render);
            },
        }
    }
</script>

<style scoped>
    .controllers {
        display: flex;
        flex-flow: row wrap;
        /*margin-bottom: 20px;*/
        width: 100%;
        height: 50px;
        align-items: center;
        justify-content: center;
    }

    .controllers-button {
        width: 250px;
        height: 40px;
        background-color: #bd2f2f;
        box-shadow: 0 5px 6px 0 rgba(0, 0, 0, 0.58);
    }

    .controllers-button:hover {
        background-color: #c34242;
        position: relative;
    }
</style>