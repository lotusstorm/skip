<template>
    <transition>
        <div class="global-loader">
            <div class="global-loader__content"></div>
        </div>
    </transition>
</template>

<script>
    export default {
        name: "GlobalLoadComponent"
    }
</script>

<style scoped>
    .global-loader {
        width: 100%;
        height: 100%;
        position: absolute;
        background-color: black;
        opacity: 50%;
    }
</style>