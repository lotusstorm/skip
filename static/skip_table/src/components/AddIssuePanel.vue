<template>
    <div class="add-issue">
        <div class="add-issue__wrapper">
            <input
                    type="text"
                    class="add-issue__input"
                    placeholder="issue name..."
                    v-model="value"
            >
            <input
                    id="add-issue__id"
                    type="button"
             >
            <label
                    for="add-issue__id"
                    :class="['add-issue__button', {'disable' : value === ''}]"
                    @click="AddBug"
            >
                <span :class="['add-issue__content', modifier]" v-if="!show"></span>
                <img
                        v-if="show"
                        src="../assets/Spinner-1s-200px_white.svg"
                        alt=""
                        class="add-issue__img"
                >
            </label>

        </div>
    </div>
</template>

<script>
    export default {
        name: "AddIssuePanel",
        data() {
            return {
                value: '',
            }
        },
        props: {
            'show': Boolean,
            'modifier': String,
        },
        methods: {
            /**
             * Метод для взомодействия дочернего компонента с родительским
             */
            AddBug() {
                this.$emit('event', event.target, this.value.toString().toUpperCase());
                this.value = ''
            },
        }
    }
</script>

<style scoped>
    #add-issue__id {
        display: none;
    }

    .add-issue {
        display: flex;
        flex-flow: row wrap;
        background-color: var(--add-panel-bg-color);
        height: 45px;
    }

    .add-issue__wrapper {
        display: flex;
        flex-flow: row wrap;
        width: 100%;
        height: 100%;
    }

    .add-issue__input {
        box-sizing: border-box;
        padding: 2px 2px 2px 10px;
        background-color: var(--add-panel-input-bg-color);
        border: 2px solid var(--add-panel-input-border-color);
        border-right: none;
        color: var(--add-panel-input-text-color);
        flex-grow: 1;
        height: 100%;
    }

    .add-issue__input::placeholder {
        color: var(--add-panel-input-placeholder-color);
        opacity: 0.5;
        font-size: 15px;
        padding-left: 2px;
    }

    .add-issue__button {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100px;
        height: 100%;
        background-color: var(--add-panel-add-btn-bg-color);
        color: var(--add-panel-add-btn-text-color);
    }

    .add-issue__button:hover {
        color: var(--add-panel-add-btn-text-color-hover);
        background-color: var(--add-panel-add-btn-bg-color-hover);
    }

    .add-issue__button:disabled {
        color: var(--add-panel-add-btn-text-color-hover);
        background-color: #c36e70;
        border: 2px solid var(--add-panel-add-btn-border-color-hover);
    }

    .add-issue__img {
        width: 40px;
    }

    .disable {
        pointer-events:none;
        background-color: #c36e70 !important;
    }

</style>