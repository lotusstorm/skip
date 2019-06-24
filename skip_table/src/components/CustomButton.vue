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
        width: 40px;
        height: 40px;
        background-color: var(--custom-btn-bg-color);
        color: var(--custom-btn-icon-color);
        cursor: pointer;
    }

    .controls-button-container:hover {
        background-color: var(--custom-btn-bg-color-hover);
        color: var(--custom-btn-icon-color-hover);
    }

    .controls-button-custom {
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
        border: none;
        width: 100%;
        height: 100%;
    }
</style>