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
        <app-controllers-button
                :disabled="getData.length === 0"
                @event="getReport"
                :modifier="'download'"
                :description="'Report'"
        ></app-controllers-button>
    </div>
</template>

<script>
    import {distributor, HTTP, HTTP_2} from '../store/globalSettings'
    import { mapActions, mapGetters } from 'vuex'
    import ControllersButton from '@/components/ControllersButton.vue'


    export default {
        name: "Controllers",
        data() {
            return {
                url: HTTP_2,
                store: []
            }
        },
        computed: {
            ...mapGetters([
                'getData',
                'getBranch',
                'getOs',
            ]),
        },
        components: {
            'app-controllers-button': ControllersButton,
        },
        methods: {
            ...mapActions([
                'loadGlobalLoaderShow',
                'loadData',
                'loadSelected',
                'actionSetData',
            ]),
            /**
             * Сохраняет изменения на клиенте в БД
             */
            save() {
                let select = {
                    id: null,
                    status: false,
                    data: []
                };

                this.loadGlobalLoaderShow(true);
                HTTP.put('/global_update', {
                        branch: this.getBranch,
                        data: this.getData,
                        os: this.getOs,
                    })
                    .then((response) => {
                        let data = response.data.data;
                        distributor(data, this.getData, true);
                        this.actionSetData(data);
                        this.loadSelected(select);
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
                let select = {
                    id: null,
                    status: false,
                    data: []
                };

                let data = {
                    branch: this.getBranch,
                    os: this.getOs
                };

                this.loadData({'data': data, 'old_data': this.getData, 'cache': true});
                this.loadSelected(select);
            },
            getReport() {
                HTTP_2.post("/generate_report")
                      .then((response) => {
                          const url = window.URL.createObjectURL(new Blob([response.data], {type: 'text/xls'}));
                          const link = document.createElement('a');
                          link.href = url;
                          link.setAttribute('download', 'report.xls');
                          document.body.appendChild(link);
                          link.click();
                      });
            },
        }
    }
</script>

<style scoped>
    .controllers {
        display: flex;
        flex-flow: row wrap;
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