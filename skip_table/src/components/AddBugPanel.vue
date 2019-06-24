<template>
    <div class="add-bug">
        <div class="add-bug__wrapper">
            <input
                    type="text"
                    class="add-bug__input"
                    placeholder="issue name..."
                    v-model="value"
            >
            <input
                    :disabled="value === ''"
                    type="button"
                    value="add"
                    class="add-bug__button"
                    @click="AddBug"
            >
        </div>
    </div>
</template>

<script>
    export default {
        name: "AddBugPanel",
        data() {
            return {
                value: ''
            }
        },
        methods: {
            AddBug() {
                this.$emit('event', event.target, this.value.toString().toUpperCase());
                this.value = ''
            },
        }
    }
</script>

<style scoped>
    .add-bug {
        display: flex;
        flex-flow: row wrap;
        background-color: var(--add-panel-bg-color);
        height: 45px;
    }

    .add-bug__wrapper {
        display: flex;
        flex-flow: row wrap;
        margin: 0 0 5px;
        width: 100%;
        height: 100%;
    }

    .add-bug__input {
        box-sizing: border-box;
        padding: 2px 2px 2px 10px;
        background-color: var(--add-panel-input-bg-color);
        border: 2px solid var(--add-panel-input-border-color);
        border-right: none;
        color: var(--add-panel-input-text-color);
        flex-grow: 1;
        height: 100%;
    }

    .add-bug__input::placeholder {
        color: var(--add-panel-input-placeholder-color);
        opacity: 0.5;
        font-size: 15px;
        padding-left: 2px;
    }

    .add-bug__button {
        width: 100px;
        height: 100%;
        background-color: var(--add-panel-add-btn-bg-color);
        border: 2px solid var(--add-panel-add-btn-border-color-hover);
        color: var(--add-panel-add-btn-text-color);
    }

    .add-bug__button:hover {
        color: var(--add-panel-add-btn-text-color-hover);
        background-color: var(--add-panel-add-btn-bg-color-hover);
        border: 2px solid var(--add-panel-add-btn-border-color-hover);
    }

    .add-bug__button:disabled {
        color: var(--add-panel-add-btn-text-color-hover);
        /*background-color: var(--add-panel-add-btn-bg-color-hover);*/
        background-color: #c36e70;
        border: 2px solid var(--add-panel-add-btn-border-color-hover);
    }

</style>