<template>
    <div class="branches">
        <div class="branches__wrapper"></div>
        <ul class="nav">
            <li
                    class="nav__item"
                    @click="selectBranch"
            >
                <p
                        class="nav__content"
                        id="development"
                >DEV</p>
            </li>
            <li
                    class="nav__item"

                    @click="selectBranch"
            >
                <p
                        class="nav__content"
                        id="an-minor"
                >AN-MINOR</p>
            </li>
            <li
                    class="nav__item"
                    @click="selectBranch"
            >
                <p
                        class="nav__content"
                        id="an-weekly"
                >AN-WEEKLY</p>
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
            ]),
        },
        methods: {
            ...mapActions([
                'loadBranch',
                'loadTests',
                'loadSteps',
                'loadBugs',
                'loadModules',
                'loadTestCategory',
                'loadStepCategory',
                'loadModuleCategory',
                'loadSelected',

            ]),
            selectBranch(event) {
                let data = {
                    id: null,
                    status: false
                };
                if (this.getBranch !== event.target.id) {
                    if (confirm('все не сохраненные действия будут сброшенны, принять??')) {
                        this.loadModuleCategory(data);
                        this.loadTestCategory(data);
                        this.loadStepCategory(data);
                        this.loadSelected(data);
                        this.loadBranch(event.target.id);
                        this.loadModules(this.getBranch);
                        this.loadTests(this.getBranch);
                        this.loadSteps(this.getBranch);
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
        height: 100%;
        align-items: center;
        justify-content: center;
        background-color: #2a3744;
        border-right: 3px solid #2a3744;
        box-sizing: content-box;
        margin-right: 10px;
    }

    .branches__wrapper {
        display: flex;
        flex-flow: row wrap;
        height: 100%;
    }

    .nav {
        display: flex;
        flex-direction: column;
        width: 100%;

    }

    .nav__item {
        display: flex;
        flex-flow: row wrap;
        height: 50px;
        width: 100%;
        box-sizing: content-box;
        background-color: #bd2f2fde;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
    }

    .nav__item:hover {
        /*border-right: 3px inset #2a3744;*/
        border-right: 3px inset #bd2f2fde;
        background-color: #2a3744;
        box-sizing: content-box;
    }

    .nav__content {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        color: #f0f0f0;
        margin: 5px 5px 5px 8px;
        font-size: 10px;
        width: 100%;
        height: 100%;
    }
</style>