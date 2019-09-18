<template>
    <li :id="id" :class="modifier">
        <div class="issue__wrapper" @click="Event">
            <p class="issue-content">{{ data.name }}</p>
            <span class="issue-status">{{ data.status }}</span>
        </div>
        <slot></slot>
    </li>
</template>

<script>
    export default {
        name: "IssueSettings",
        props: {
            'checked': Boolean,
            'data': Object,
            'id': Number,
            'modifier': String,
        },
        methods: {
            Event() {
                this.$emit('event', this.id);
            }
        },
    }

</script>

<style scoped>
    .issue__wrapper {
        display: flex;
        flex-grow: 1;
        margin-left: 10px;
        cursor: pointer;
        height: 100%;
        align-items: center;
        justify-content: space-between;
    }

    .issue-status {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #2ab192b3;
        color: #f0f0f0;
        padding: 2px 4px;
        font-size: 15px;
        border-radius: 3px;
        margin-right: 10px;
    }

</style>