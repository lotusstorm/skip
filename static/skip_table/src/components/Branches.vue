<template>
    <div class="branches">
        <ul class="nav" @click="selectBranch">
            <li class="nav__item" data-id="development">
                <p class="nav__content" data-id="development">DEV</p>
            </li>
            <li class="nav__item" data-id="an-minor">
                <p class="nav__content" data-id="an-minor">AN-MINOR</p>
            </li>
            <li class="nav__item" data-id="an-weekly">
                <p class="nav__content" data-id="an-weekly">AN-WEEKLY</p>
            </li>
        </ul>
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
                    status: false
                };

                let render = {
                    data: [],
                };

                if (this.getBranch !== event.target.dataset.id) {
                    if (confirm('все не сохраненные действия будут сброшенны, принять??')) {
                        this.loadSelected(select);
                        this.loadBranch(event.target.dataset.id);

                        let data = {
                            branch: this.getBranch,
                            os: this.getOs
                        };

                        this.loadData(data);
                        this.loadTestRender(render);
                    }
                }
            },
        }
    }
</script>

<style scoped>
    .branches {
        display: flex;
        flex-flow: row wrap;
        width: 60px;
        align-items: center;
        justify-content: center;
        background-color: #2a3744;
        border-right: 3px solid #2a3744;
        box-sizing: content-box;
        margin-right: 10px;
        flex-grow: 0;
    }

    .nav {
        display: flex;
        flex-direction: column;
    }

    .nav__item {
        display: flex;
        flex-flow: row wrap;
        justify-content: flex-start;
        height: 50px;
        width: 100%;
        box-sizing: content-box;
        background-color: #bd2f2fde;
        align-items: center;
        cursor: pointer;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
    }

    .nav__item:hover {
        border-right: 3px inset #bd2f2fde;
        background-color: #2a3744;
        box-sizing: content-box;
    }

    .nav__content {
        display: flex;
        color: #f0f0f0;
        margin: 2px 2px 2px 5px;
        font-size: 12px;
    }
</style>