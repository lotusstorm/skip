<template>
    <div class="search">
        <input
                type="text"
                @input="searchWithInput"
                class="search-textbox"
                id="Search"
                placeholder="search..."
                autocomplete="off"
                :value="getSearchValue"
        >
        <input
                type="button"
                id="search-button"
        >
        <label
                for="search-button"
                class="search-button-custom"
                @click.prevent="searchWithButton"
        ></label>
    </div>
</template>

<script>
    export default {
        name: "Search",
        props: {
            searchAction: Function,
            getSearchValue: String,
        },
        methods: {
            searchWithInput(event) {
                this.searchAction(event.target.value);
            },
            searchWithButton() {
                //TODO поиск по нажатию на кнопку хз зачем ¯\_(ツ)_/¯
                console.log("¯\\_(ツ)_/¯");
            },
        }
    }
</script>

<style scoped>
    .search {
        box-sizing: border-box;
        display: flex;
        flex-flow: row wrap;
        border: 5px solid var(--search-border-color);
        height: 50px;
        width: 100%;
    }

    .search-textbox::placeholder {
        color: var(--search-placeholder-color);
        opacity: 0.5;
        font-size: 18px;
        padding-left: 2px;
    }

    .search-textbox {
        box-sizing: border-box;
        padding: 2px 2px 2px 10px;
        flex-grow: 1;
        height: 100%;
        font-size: 20px;
        border: none;
        background-color: var(--search-text-input-bg-color);
        color: var(--search-text-color);
    }

    #search-button {
        display: none;
    }

    .search-button-custom {
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
        border: none;
        width: 50px;
        height: 100%;
        background-color: var(--search-btn-bg-color);
        color: var(--search-text-color);
        cursor: pointer;
    }

    .search-button-custom:before {
        font-family: icomoon;
        content: var(--search-icon);
        font-size: 20px;

    }

    .search-button-custom:hover {
        background-color: var(--search-btn-hover-color);
        color: var(--search-text-hover-color);
        border: 2px solid var(--search-btn-border-hover-color)
    }
</style>