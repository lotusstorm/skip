<template>
    <div id="app">
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
            let data = {
                branch: this.getBranch,
                os: this.getOs
            };

            this.$store.dispatch('loadData', data);
            this.$store.dispatch('loadIssues');
        },
        computed: {
            ...mapGetters([
                'getBranch',
                'getOs',
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
        --main-bg-color-gradient: linear-gradient(180deg, rgba(35, 111, 140, 0.45) 0%, rgb(30, 61, 96) 100%) 70%;
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

        /************ISSUE-DESCRIPTION******************/
        --issue-summary-text-color: #384857;
        --issue-summary-title-text-color: #f0f0f0;
        --issue-summary-bg-color: #f0f0f0;
        --issue-summary-row-bg-color: #f0f0f0;


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
        --add-panel-input-bg-color: #384857;
        --add-panel-input-text-color: #f0f0f0;
        --add-panel-input-border-color: #384857;
        --add-panel-input-placeholder-color: #f0f0f0;
    }

    *, li, p, h1, h2, h3, span {
        font-family: "Ubuntu", Arial, "Helvetica Neue", Helvetica, sans-serif;
        font-weight: 500;
    }

    html, body {
        width: 100%;
        height: 100%;
    }

    /************************************************************/

    #app {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: var(--main-bg-color);
        width: 100%;
        height: 100%;
    }

    .app-content {
        display: flex;
        flex-flow: row;
        width: 100%;
        height: 100%;
    }

    .main-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        flex-grow: 1;
        height: 100%;
    }

    .app-wrapper {
        display: flex;
        flex-flow: row wrap;
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        justify-content: space-around;
        text-align: center;
        width: 100%;
        flex-grow: 1;
        overflow: auto;
    }

    .table {
        display: flex;
        flex-direction: column;
        /* margin-bottom: 8px; */
        width: 545px;
        height: 95%;
        max-height: 800px;
        max-width: 560px;
        background-color: var(--table-bg-color);
        border: var(--table-bg-border-color);
        box-shadow: 0 8px 10px 2px rgba(0, 0, 0, 0.58);
        /* margin-top: 8px; */
        flex: 1;
        margin: 8px 4px;
    }

    .table__wrapper {
        display: flex;
        flex-direction: column;
        height: 450px;
        flex: 1;
    }

    .table__title {
        height: 50px;
        min-height: 50px;
        display: flex;
        justify-content: center;
        background-color: var(--title-bg-color);
        border-bottom: 2px solid var(--title-border-color);
        color: var(--title-text-color);
    }

    .table__title-content {
        display: flex;
        font-size: 30px;
        align-items: center;
    }

    .table__content-list {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        width: 100%;
        height: 100%;
        margin-top: 2px;
        overflow: auto;
        background-color: var(--items-list-bg-color);
    }

    .table__content-item {
        display: flex;
        flex-flow: row;
        box-sizing: content-box;
        align-items: center;
        width: 450px;
        height: 40px;
        min-width: 370px;
        min-height: 40px;
        font-size: 30px;
        border-radius: 5px;
        margin: 0 0 0 30px;
        cursor: pointer;
    }

    .table__content-item:hover {
        position: relative;
        width: 460px;
        right: 5px;
    }

    .description {
        display: flex;
        flex-grow: 1;
        padding-left: 10px;
        height: 100%;
        align-items: center;
    }

    .active {
        background-color: var(--item-bg-color-active) !important;
        color: var(--item-text-color-active) !important;
        transition: background-color ease .5s;
    }

    .table__content-wrapper {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 100%;
        overflow: auto;
    }

    input[type=checkbox], input[type=radio] {display: none;}

    input[type=checkbox] + label:before {
        font-family: icomoon;
        content: "\e999";
        font-size: 20px;
        color: #f5f5f5;
        position: relative;
        left: 5px;
        border-radius: 2px;
        display: inline-block;
        border: 6px solid #f5f5f5;
        margin: -5px 5px 0 0;
        height: 20px;
        width: 20px;
        background-color: #f5f5f5;
        box-sizing: content-box;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }

    input[type=checkbox]:checked + label:before {
        font-family: icomoon;
        content: "\e999";
        font-size: 20px;
        color: #2A3744;
    }

    /******************************************/
    .update-all-button:before {
        font-family: icomoon;
        content: var(--all-update-btn-icon);
        font-size: 20px;
    }

    .add-panel-button:before {
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
        background-color: #bd2f2fde;
        color: #F0F0F0;
    }

    .category--style:hover {
        background-color:  #c34242;
        color: #F0F0F0;
    }

    .component--style {
        background-color: #2ab192b3;
        color: #F0F0F0;
    }

    .component--style:hover {
        background-color: #4bdcbba8;
        color: #F0F0F0;
    }

    .module--style {
        background-color: var(--item-bg-color);
        color: var(--item-text-color);
    }

    .module--style:hover {
        background-color: var(--item-bg-color);
        color: var(--item-text-color);
    }

    .test--style {
        background-color: rgba(231, 201, 66, 0.98);
        color: #F0F0F0;
    }

    .test--style:hover {
        background-color: rgba(217, 191, 63, 0.96);
        color: #F0F0F0;
    }

    .step--style {
        background-color: var(--item-bg-color);
        color: var(--item-text-color);
    }

    .step--style:hover {
        background-color: var(--item-bg-color-hover);
        color: var(--item-text-color-hover);
    }

    .issue--style {
        background-color: var(--item-bg-color);
        color: var(--item-text-color);
        width: 85%;
        height: 40px !important;
        margin-top: 5px;
    }

    .issue--style:hover {
        background-color: var(--item-bg-color-hover);
        color: var(--item-text-color-hover);
        width: 88%;

    }

    .disable {
        pointer-events: none;
        opacity: .5 !important;
    }

    .modules {
        min-width: 525px;
    }

    .tests {
        min-width: 525px;
    }

    .issue {
        min-width: 460px;
    }

</style>
