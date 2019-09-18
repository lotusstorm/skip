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
    @import "../public/colors.css";

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
        width: 545px;
        height: 95%;
        max-height: 800px;
        max-width: 560px;
        background-color: var(--table-bg-color);
        border: var(--table-bg-border-color);
        box-shadow: 0 8px 10px 2px rgba(0, 0, 0, 0.58);
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
        margin: 2px 0 2px 30px;
        cursor: pointer;
        color: var(--item-text-color);
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

    .collapse-button-active {
        color: var(--collapse-btn-active-color) !important;
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
        content: var(--checkbox-icon);
        font-size: 20px;
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

    .update-all-button,
    .single-delete-button,
    .single-update-button,
    .hide-description-button,
    .collapse-button {
        font-family: icomoon;
        font-size: 20px;
        height: 40px;
        width: 40px;
        color: var(--item-text-color); 
        cursor: pointer;
    }

    .single-update-button:hover,
    .hide-description-button:hover {
        color:#e7c942fa;
    }

    .single-delete-button:hover {
        color:#bd2f2f;
    }

    .collapse-button:hover {
        color:#384857;
    }

    .add-panel-button:before {
        content: var(--show-add-panel-btn-icon);
        font-family: icomoon;
        font-size: 20px;
    }

    .single-delete-button:before {
        content: var(--single-delete-btn-icon);
    }

    .single-update-button:before {
        content: var(--single-update-icon);
    }

    /* .show-description-button:before {
        content: var(--show-description-icon);
    } */

    .hide-description-button:before {
        content: var(--hide-description-icon);
    }

    .collapse-button:before {
        content: var(--collapse-btn-icon);
    }

    .category--style {
        background-color: var(--category-style);
    }

    .category--style:hover {
        background-color:  var(--category-hover-style);
    }

    .component--style {
        background-color: var(--component-style);
    }

    .component--style:hover {
        background-color: var(--component-hover-style);
    }

    .module--style {
        background-color: var(--module-style);
    }

    .module--style:hover {
        background-color: var(--module-hover-style);
    }

    .test--style {
        background-color: var(--test-style);
    }

    .test--style:hover {
        background-color: var(--test-hover-style);
    }

    .step--style {
        background-color: var(--step-style);
    }

    .step--style:hover {
        background-color: var(--step-hover-style);
    }

    .issue--style {
        background-color: var(--issue-style);
        width: 85%;
        height: 40px !important;
    }

    .issue--style:hover {
        background-color: var(--issue-hover-style);
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
