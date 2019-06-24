<template>
    <div class="header">
        <div class="current-branch">{{ getBranch }}</div>
        <div class="header__wrapper">
            <ul class="nav">
                <li
                        class="nav__item"
                        @click="to('home')"
                >
                    <p class="nav__content">Home</p>
                </li>
                <li
                        @click="to('items')"
                        class="nav__item"
                >
                    <p class="nav__content">DB-Settings</p>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex'

    export default {
        name: "Header",
        computed: {
            ...mapGetters([
                'getBranch',
            ]),
        },
        methods: {
            ...mapActions([
                'loadSelected',
                'loadHomeBugsFilter',
            ]),
            to(to) {
                this.$router.push({ name: to});

                let data = {
                    id: null,
                    status: false
                };
                this.loadSelected(data);
                this.loadHomeBugsFilter('all');
            }
        }
    }
</script>

<style scoped>
    .header {
        display: flex;
        flex-flow: row wrap;
        width: 100%;
        height: 50px;
        align-items: center;
        justify-content: center;
        background-color: #2a3744;
        border-bottom: 3px solid #2a3744;
        box-sizing: content-box;
    }

    .header__wrapper {
        display: flex;
        flex-flow: row wrap;
        height: 100%;
    }

    .nav {
        display: flex;
        flex-flow: row wrap;
        height: 100%;

    }

    .nav__item {
        display: flex;
        flex-flow: row wrap;
        height: 100%;
        width: 100px;
        box-sizing: content-box;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }

    .nav__item:hover {
        border-bottom: 3px inset #bd2f2f;
        background-color: #384857;
        box-sizing: content-box;
    }

    .nav__content {
        color: #f0f0f0;
    }

    .current-branch {
        padding: 3px 5px;
        background-color: #bd2f2f;
        border-radius: 5px;
        color: #f0f0f0;
        margin: 0 10px;
    }

</style>