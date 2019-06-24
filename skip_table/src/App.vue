<template>
    <div id="app">
<!--        -->
        <app-global-load-component v-if="getGlobalLoaderShow"></app-global-load-component>
        <app-header></app-header>
        <router-view/>
    </div>
</template>

<script>
    import Header from '@/components/Header.vue'
    import GlobalLoadComponent from '@/components/GlobalLoadComponent.vue'
    import { mapGetters } from 'vuex'


    export default {
        components: {
            'app-header': Header,
            'app-global-load-component': GlobalLoadComponent,
        },
        created() {
            this.$store.dispatch('loadModules', this.getBranch);
            this.$store.dispatch('loadTests', this.getBranch);
            this.$store.dispatch('loadSteps', this.getBranch);
            this.$store.dispatch('loadBugs');
        },
        computed: {
            ...mapGetters([
                'getBranch',
                'getGlobalLoaderShow',
            ]),
        },
    }
</script>



<style>
    @import "../public/fonts.css";
    @import "../public/reset.css";

    :root {
        /************MAIN-BG******************/
        --main-bg-color: #b5ced8b8;
        --main-bg-color-gradient: linear-gradient(180deg, rgba(35, 111, 140, 0.45) 0%,
        rgb(30, 61, 96) 100%) 70%;
        /************SHOW-DESCRIPTION-BTN******************/
        --show-description-icon: "\e9cf";

        /************HIDE-DESCRIPTION-BTN******************/
        --hide-description-icon: "\e9d0";

        /************SINGLE-UPDATE-BTN******************/
        --single-update-icon: "\e984";

        /************ALL-UPDATE-BTN******************/
        --all-update-btn-icon:  "\e984";

        /************SHOW-ADD-PANEL-BTN******************/
        --show-add-panel-btn-icon:  "\ea0a";

        /************SINGLE-DELETE-BTN******************/
        --single-delete-btn-icon:  "\ea0f";

        /********************CUSTOM-BTN*******************/
        --custom-btn-icon-color: #f0f0f0;
        --custom-btn-icon-color-hover: #f0f0f0;
        --custom-btn-bg-color: #384857;
        --custom-btn-bg-color-hover: #516a7c;

        /************CONTROLS-BTN******************/
        --controls-btn-icon-color: #f0f0f0;
        --controls-btn-icon-color-hover: #2a3744;
        --controls-btn-bg-color: #2a3744;
        --controls-btn-bg-color-hover: #f0f0f0;
        --controls-btn-border-color-hover: #2a3744;

        /************SEARCH******************/
        --search-icon: "\e986";
        --search-icon-color: #f0f0f0;
        --search-text-input-bg-color: #384857;
        --search-btn-bg-color: #2a3744;
        --search-border-color: #2a3744;
        --search-text-color: #f0f0f0;
        --search-text-hover-color: #f0f0f0;
        --search-placeholder-color: #f0f0f0;
        --search-btn-hover-color: #2a3744;
        --search-btn-border-hover-color: #2a3744;

        /************BUG-DESCRIPTION******************/
        --bug-description-text-color: #384857;
        --bug-description-title-text-color: #f0f0f0;
        --bug-description-bg-color: #f0f0f0;
        --bug-description-row-bg-color: #f0f0f0;


        /************TITLE******************/
        --title-bg-color: #2a3744;
        --title-text-color: #f0f0f0;
        --title-border-color: #2a3744;


        /************TABLE******************/
        --table-bg-color: #2a3744;
        --table-box-shadow: 0 0 25px rgba(0,0,0,0.25);
        --table-bg-border-color: 1px solid #2a3744;

        /************ITEMS-LIST******************/
        --items-list-bg-color: #2a3744;

        /************ITEM******************/
        --item-bg-color: #384857;
        --item-bg-color-hover: #516a7c;
        --item-bg-color-active: #f0f0f0;
        --item-text-color: #f0f0f0;
        --item-text-color-hover: #f0f0f0;
        --item-text-color-active: #2a3744;
        --item-border-color: #2a3744;
        --item-border-color-hover: #2a3744;
        --item-border-color-active: #2a3744;
        --item-box-shadow-hover: -5px 5px 5px rgba(0,0,0,0.25);

        /************FILTER******************/
        --filter-bg-color: #2a3744;
        --filter-bg-border-color: #384857;
        --filter-btn-color: #384857;
        --filter-btn-color-hover: #516a7c;
        --filter-btn-color-active: #f0f0f0;
        --filter-btn-border-color-hover: #2a3744;
        --filter-btn-border-color-active: #2a3744;
        --filter-btn-border-color: #2a3744;
        --filter-btn-text-color: #f0f0f0;
        --filter-btn-text-color-hover: #f0f0f0;
        --filter-btn-text-color-active: #2a3744;

        /************ADD-PANEL******************/
        --add-panel-bg-color: #2A3744;
        --add-panel-add-btn-bg-color: #bd2f2f;
        --add-panel-add-btn-bg-color-hover: #c34242;
        --add-panel-add-btn-border-color-hover: #2a3744;
        --add-panel-add-btn-text-color: #f0f0f0;
        --add-panel-add-btn-text-color-hover: #f0f0f0;
        --add-panel-input-bg-color: #2a3744;
        --add-panel-input-text-color: #f0f0f0;
        --add-panel-input-border-color: #2a3744;
        --add-panel-input-placeholder-color: #f0f0f0;
    }

    *, li {
        font-family: "Ubuntu", Arial, "Helvetica Neue", Helvetica, sans-serif;
        font-weight: 500;
    }

    html, body {
        width: 100%;
        height: 100%;
    }


    /*****************************SCROLL BAR*********************/
    /*::-webkit-scrollbar {*/
    /*    width: 3px;*/
    /*    height: 3px;*/
    /*}*/

    /*::-webkit-scrollbar-button {*/
    /*    background-color: #ef2551;*/
    /*}*/

    /*::-webkit-scrollbar-track {*/
    /*    background-color: #1f9947;*/
    /*}*/

    /*::-webkit-scrollbar-track-piece {*/
    /*    background-color: #5c60ff;*/
    /*}*/

    /*::-webkit-scrollbar-thumb {*/
    /*    height: 50px;*/
    /*    background-color: #4a6642;*/
    /*    border-radius: 3px;*/
    /*}*/

    /*::-webkit-scrollbar-corner {*/
    /*    background-color: #996f29;*/
    /*}*/

    /*::-webkit-resizer {*/
    /*    background-color: #216658;*/
    /*}*/

    /************************************************************/


    #app {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        height: 100%;
        background-color: var(--main-bg-color);
        /*background: var(--main-bg-color-gradient);*/
    }

    .app-content {
        display: flex;
        flex-flow: row;
        /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
        /*justify-content: space-around;*/
        /*text-align: center;*/
        width: 100%;
        height: 100%;
        /*margin-top: 15px;*/
    }

    .app_wrapper {
        display: flex;
        flex-flow: row wrap;
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        justify-content: space-around;
        text-align: center;
        width: 100%;
        height: 100%;
        /*margin-top: 15px;*/
    }

    .table {
        display: flex;
        flex-direction: column;
        margin-bottom: 8px;
        width: 600px;
        height: 80%;
        background-color: var(--table-bg-color);
        border: var(--table-bg-border-color);
        box-shadow: 0 8px 15px 2px rgba(0, 0, 0, 0.58);
        margin-top: 8px;
    }

    .table_wrapper {
        display: flex;
        flex-direction: column;
        height: 450px;
        flex: 1;
    }

    .title {
        height: 50px;
        display: flex;
        justify-content: center;
        background-color: var(--title-bg-color);
        border-bottom: 2px solid var(--title-border-color);
        color: var(--title-text-color);
    }

    .content {
        display: flex;
        font-size: 30px;
        align-items: center;
    }

    .list {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: var(--items-list-bg-color);
    }

    .item {
        display: flex;
        flex-flow: row;
        box-sizing: content-box;
        align-items: center;
        width: 85%;
        height: 40px;
        font-size: 30px;
        background-color: var(--item-bg-color);
        color: var(--item-text-color);
        border-radius: 5px;
        margin: 0 0 0 30px;
        border: 2px solid var(--item-border-color);
        cursor: pointer;
    }

    .description {
        display: flex;
        flex-grow: 1;
        margin-left: 10px;
        height: 40px;
        align-items: center;
    }

    .item:hover {
        background-color: var(--item-bg-color-hover);
        color: var(--item-text-color-hover);
        position: relative;
        width: 87%;
        right: 5px;
    }

    .active {
        background-color: var(--item-bg-color-active);
        border: 2px solid var(--item-border-color-active);
        color: var(--item-text-color-active);
    }

    .controllers {
        display: flex;
        flex-flow: row wrap;
    }

    .content-wrapper {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 100%;
        overflow: auto;
    }

    /*input[type=checkbox] {display: none;}*/
    input[type=checkbox] {
        width: 40px;
        height: 40px;
    }

    /*input[type=checkbox] + label:before {*/
    /*    content: "\2713";*/
    /*    color: transparent;*/
    /*    display: inline-block;*/
    /*    border: 1px solid #000;*/
    /*    font-size: 20px;    */
    /*    line-height: 22px;*/
    /*    margin: -5px 5px 0 0;*/
    /*    height: 20px;*/
    /*    width: 20px;*/
    /*    text-align: center;*/
    /*    vertical-align: middle;*/
    /*    transition: color ease .3s;*/
    /*}*/

    /*input[type=checkbox]:checked + label:before {*/
    /*    color: #000;*/
    /*}*/


    /******************************************/
    .update-all-button:before {
        font-family: icomoon;
        content: var(--all-update-btn-icon);
        font-size: 20px;
    }

    .show-add-panel-button:before {
        font-family: icomoon;
        content: var(--show-add-panel-btn-icon);
        font-size: 20px;
    }

    .single-delete-button:before {
        font-family: icomoon;
        content: var(--single-delete-btn-icon);
        font-size: 20px;
    }

    .single-update-button:before {
        font-family: icomoon;
        content: var(--single-update-icon);
        font-size: 20px;
    }

    .show-description-button:before {
        font-family: icomoon;
        content: var(--show-description-icon);
        font-size: 20px;
    }

    .hide-description-button:before {
        font-family: icomoon;
        content: var(--hide-description-icon);
        font-size: 20px;
    }

    .category--style {
        background-color: #bd2f2fde !important;
    }

    .category--style:hover {
        background-color:  #c34242 !important;
    }

    .component--style {
        background-color: #2ab192b3 !important;
    }

    .component--style:hover {
        background-color: #4bdcbba8 !important;
    }

</style>
