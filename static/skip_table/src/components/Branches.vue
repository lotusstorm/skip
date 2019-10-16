<template>
    <div class="branches">
        <ul class="nav" @click="selectBranch">
            <li class="nav__item" data-id="an-prestable">
                <p class="nav__content" data-id="an-prestable">AN-PRESTABLE</p>
            </li>
            <li class="nav__item" data-id="an-minor">
                <p class="nav__content" data-id="an-minor">AN-MINOR</p>
            </li>
            <li class="nav__item" data-id="an-weekly">
                <p class="nav__content" data-id="an-weekly">AN-WEEKLY</p>
            </li>
        </ul>
        <div class="version">
            <h1 class="version-content">v.2.0.1.1</h1>
        </div>
    </div>
</template>

<script>
    import { mapActions, mapGetters } from 'vuex'


    export default {
        name: "Branches",
        computed: {
            ...mapGetters([
                'getBranch',
                'getOs',
                'getData',
            ]),
        },
        methods: {
            ...mapActions([
                'loadBranch',
                'loadData',
                'loadSelected',
                'loadTestRender',
            ]),
            /**
             * Метод для выбора нужной ветки
             * @param event - событие мыши
             */
            selectBranch(event) {
                let select = {
                    id: null,
                    status: false,
                    data: []
                };

                if (this.getBranch !== event.target.dataset.id && event.target.dataset.id != undefined) {
                    if (confirm(`Переход на ветку ${event.target.dataset.id.toUpperCase()} все не сохраненные действия будут сброшенны, принять??`)) {
                        this.loadSelected(select);
                        this.loadBranch(event.target.dataset.id);

                        let data = {
                            branch: this.getBranch,
                            os: this.getOs
                        };

                        this.loadData({'data': data, 'old_data': this.getData, 'cache': false});
                    }
                }
            },
        }
    }
</script>

<style scoped>
    .branches {
        display: flex;
        flex-direction: column;
        width: 150px;
        min-width: 110px;
        background-color: #2a3744;
        box-sizing: content-box;
        height: 100%;
    }

    .nav {
        display: flex;
        flex-direction: column;
        width: 100%;
        flex-grow: 1;
    }

    .nav__item {
        display: flex;
        flex-flow: row wrap;
        justify-content: flex-start;
        height: 50px;
        box-sizing: content-box;
        background-color: #384857;
        align-items: center;
        cursor: pointer;
        border-bottom: 2px inset #384857;
    }

    .nav__item:hover {
        border-bottom: 2px inset #bd2f2fde;
        background-color: #2a3744;
        box-sizing: content-box;
        transition: background-color ease .5s;
    }

    .nav__content {
        display: flex;
        color: #f0f0f0;
        margin: 2px 2px 2px 10px;
        font-size: 16px;
        font-weight: normal;
    }

    .version {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        background-color: #bd2f2fde;
    }

    .version-content {
        color: #f0f0f0;
        padding: 2px 4px;
    }
</style>