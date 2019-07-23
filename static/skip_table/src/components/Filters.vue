<template>
    <div class="filters" @click="addActiveClass">
        <input
                type="button"
                value="all"
                class="filter"
        >
        <input
                type="button"
                value="checked"
                class="filter"
        >
        <input
                type="button"
                value="unchecked"
                class="filter"
        >
    </div>
</template>

<script>
    export default {
        name: "Filters",
        props: {
            filterAction: Function,
        },
        methods: {
            /**
             * Вешает css селестор .active при нажатии
             * @param event
             */
            addActiveClass(event) {
                if (event.target.className === 'filter') {
                    let element = document.querySelectorAll('.filter');
                    element.forEach(el => {
                        el.classList.remove('active');
                    });

                    event.target.classList.add('active');
                    this.filterAction(event.target.value);
                }
            },
        }
    }
</script>

<style scoped>

    .filters {
        display: flex;
        flex-flow: row wrap;
        justify-content: center;
        border-top: 2px solid var(--filter-bg-border-color);
    }

    .filter {
        box-sizing: border-box;
        border-bottom-right-radius: 5px;
        border-bottom-left-radius: 5px;
        padding: 0 5px;
        margin: 0 2px;
        color: var(--filter-btn-text-color);
        background-color: var(--filter-btn-color);
        border: 2px solid var(--filter-btn-border-color);
        border-top: none;
    }

    .filter:hover {
        color: var(--filter-btn-text-color-hover);
        background-color: var(--filter-btn-color-hover);
        border: 2px solid var(--filter-btn-border-color-hover);
        border-top: none;
    }

    .active {
        color: var(--filter-btn-text-color-active);
        background-color: var(--filter-btn-color-active);
        border: 2px solid var(--filter-btn-border-color-active);
        border-top: none;
    }

</style>