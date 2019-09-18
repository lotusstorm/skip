<template>
    <div class="controls-button-container" >
        <input
                type="button"
                id="controls-button-id"
        >
        <label
                for="controls-button-id"
                :class="['controls-button-custom', modifier]"
                @click="Event"
        ></label>
    </div>
</template>

<script>
    export default {
        name: "DeleteButton",
        props: {
            'id': Number,
            'modifier': String,
        },
        methods: {
            /**
             * Метод для взомодействия дочернего компонента с родительским
             * @constructor
             */
            Event() {
                this.$emit('event', this.id);
            }
        }
    }
</script>

<style scoped>
    #controls-button-id {
        display: none;
    }

    .controls-button-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .controls-button-custom {
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
        border: none;
    }
</style>