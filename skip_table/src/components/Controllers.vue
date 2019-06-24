<template>
    <div class="controllers">
        <app-controllers-button
                :disabled="getTests.length === 0 && getSteps.length === 0"
                @event="save"
                :modifier="'save'"
                :description="'Save'"
        ></app-controllers-button>
        <app-controllers-button
                :disabled="getTests.length === 0 && getSteps.length === 0"
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
        computed: {
            ...mapGetters([
                'getTests',
                'getSteps',
                'getBugs',
                'getBranch',
            ]),
        },
        components: {
            'app-controllers-button': ControllersButton,
        },
        methods: {
            ...mapActions([
                'loadTests',
                'loadSteps',
                'loadGlobalLoaderShow',
            ]),
            saveChanges(data, req) {

                HTTP.put(`/${req}`, {
                        branch: this.getBranch,
                        data
                    })
                    .then((response) => {
                        console.log(response.data.data);
                    })
                    .catch((error) => {
                        console.log(error);
                        console.error(`text: ${error.response.data.status}, code: ${error.response.status}`);
                    });
            },
            save() {
                this.saveChanges(this.getTests, 'tests');
                this.saveChanges(this.getSteps, 'steps');
            },

            cancel() {
                console.log('1');
                this.loadTests(this.getBranch)
                    .then(

                    );

                this.loadSteps(this.getBranch);
                // this.a('1');
                console.log('2');
                // this.loadGlobalLoaderShow(true);
                // this.loadGlobalLoaderShow(false);

                // this.a('2');

            },
        }
    }

    // function globalLoadDecorator(a) {
    //     console.log(arguments);
    //     console.log(a);
    //     return function () {
    //         console.log('1');
    //         // console.log('a', a);
    //         const a = a.apply(this, arguments);
    //         console.log(a);
    //         return a
    //     }
    // }

</script>

<style scoped>
    .controllers {
        display: flex;
        flex-flow: row wrap;
        margin-bottom: 20px;
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