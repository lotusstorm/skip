<template>
    <div :class="['controllers-button', { disabled: disabled }]">
        <input
                type="button"
                id="controllers-button-id"
        >
        <label
                for="controllers-button-id"
                :class="['controllers', modifier]"
                @click="Event"
        >{{ description }}</label>
    </div>
</template>

<script>
    export default {
        name: "ControllersButton",
        props: {
            'modifier': String,
            'description': String,
            'disabled': Boolean,
        },
        methods: {
            Event(event) {
                this.$emit('event', event.target)
            },
        },
    }
</script>

<style scoped>
    #controllers-button-id {
        display: none;
    }

    .controllers-button {
        box-sizing: border-box;
        display: flex;
        height: 40px;
        background-color: #bd2f2fde;
        color: var(--controls-btn-icon-color);

        padding: 5px;
        margin: 2px;
        border-radius: 5px;
    }

    .controllers-button:hover {
        background-color: #c34242;
        color: #f0f0f0;
    }

    .controllers {
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
        border: none;
        width: 100%;
        height: 100%;
        cursor: pointer;
    }

    .disabled {
        pointer-events:none;
        background-color: #c36e70 !important;
    }
</style>