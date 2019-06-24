<template>
    <div class="container">
        <slot></slot>
    </div>
</template>

<script>
    export default {
        name: "Container"
    }
</script>

<style scoped>
    .container {
        display: flex;
        flex-flow: row;
    }
</style>