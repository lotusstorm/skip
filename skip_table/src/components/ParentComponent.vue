<template>
    <div class="parent">
        <div class="parent__content-wrapper">
            <input
                    type="button"
                    :id="id"
                    :class="['parent__label', modifier]"
                    @click="show = !show"
                    :value="name"
            >
        </div>
        <div class="children-wrapper" v-if="show">
            <slot></slot>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                show: false
            }
        },
        name: "ParentComponent",
        props: [
            'name',
            'id',
            'modifier',
        ],
    }
</script>

<style scoped>
    .parent {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }


    .children-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        width: 95%;
        margin-top: 5px;
        margin-left: 10px;
        background-color: var(--items-list-bg-color);
    }

    .parent__label {
        display: flex;
        flex-flow: row;
        box-sizing: content-box;
        align-items: center;
        width: 75%;
        height: 40px;
        font-size: 30px;
        background-color: var(--item-bg-color);
        color: var(--item-text-color);
        border-radius: 5px;
        margin: 6px 0 4px 30px;
        border: none;
        cursor: pointer;
    }

    .parent__label:hover {
        background-color: var(--item-bg-color-hover);
        color: var(--item-text-color-hover);
        position: relative;
        width: 78%;
        right: 5px;
    }

    .parent__content-wrapper {
        display: flex;
        flex-flow: row;
        justify-content: flex-start;
        width: 100%;
    }
</style>