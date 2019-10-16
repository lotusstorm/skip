<template>
    <div class="header">
        <div class="logo">
            <h1 
                    class="logo__content" 
                    @click="to('home')"
            >
                    AUT<span class="logo__icon"></span>TESTs
            </h1>
        </div>
        <div class="header__controllers">
            <label class="select-os">
                <select
                        class="select-os__list"
                        :value="getOs"
                        @input="selectOs"
                >
                    <option
                            v-for="(el, i) in os"
                            :key="i" :value="el"
                            class="select-os__item"
                    >
                        {{ el }}
                    </option>
                </select>
            </label>
            <div class="current-branch">
                <h1 class="current-branch__content">{{ getBranch }}</h1>
            </div>
        </div>
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
        data() {
            return {
                selectedOs: 'windows',
                os: ['windows', 'linux']
            }
        },
        computed: {
            ...mapGetters([
                'getBranch',
                'getIssues',
                'getData',
                'getOs',
            ]),
        },
        methods: {
            ...mapActions([
                'loadSelected',
                'loadHomeIssuesFilter',
                'loadTestRender',
                'loadOs',
                'loadData',
            ]),

            selectOs(event) {
                let select = {
                    id: null,
                    status: false,
                    data: []
                };

                this.loadOs(event.target.value);
                this.loadSelected(select);

                let data = {
                    branch: this.getBranch,
                    os: this.getOs
                };

                this.loadData({'data': data, 'old_data': this.getData, 'cache': false});
            },
            /**
             * роутинг
             * @param to
             */
            to(to) {
                this.$router.push({ name: to});
                let select = {
                    id: null,
                    status: false,
                    data: []
                };

                this.loadHomeIssuesFilter('all');
                if (to === 'home') {
                    this.$nextTick(() => {
                        this.scrollTo('modules');
                        this.scrollTo('issues');
                        this.loadSelected(select);
                    });
                }
            },
            scrollTo(name) {
                let div = document.querySelector(`#${name}`);
                let scroll = localStorage.getItem(`${name}`) || 0;
                div.scrollTop = scroll;
            },
        }
    }
</script>

<style scoped>
    .header {
        display: flex;
        flex-flow: row wrap;
        width: 100%;
        max-height: 50px;
        min-height: 38px;
        align-items: center;
        justify-content: center;
        background-color: #2a3744;
        border-bottom: 3px solid #2a3744;
        box-sizing: content-box;
    }

    .logo {
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-sizing: content-box;
        position: absolute;
        cursor: pointer;
        left: 1%;
    }

    .logo__icon:before {
        font-family: icomoon;
        content: "\e999";
        color: #bd2f2fde;
    }

    .logo__content {
        color: #f0f0f0;
        padding: 0 3px;
    }

    .header__wrapper {
        display: flex;
        flex-flow: row wrap;
        align-items: center;
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
        display: flex;
        align-items: center;
        background-color: #bd2f2f;
        border-radius: 5px;
        color: #f0f0f0;
        height: 23px;
        margin: 0 2px;
    }

    .current-branch__content {
        margin: 0 5px;
    }

    .select-os__list {
        border-radius: 5px;
        background-color: #4bdcbba8;
        border: none;
        color: #f5f5f5;
        height: 23px;
        margin: 0 2px;
    }

    .header__controllers {
        display: flex;
        flex-flow: row;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

</style>