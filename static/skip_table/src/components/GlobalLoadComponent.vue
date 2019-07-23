<template>
    <transition>
        <div class="global-loader">
            <img class="global-loader__content" src="../assets/Spinner-1s-200px.svg" alt="">
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
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        position: absolute;
        background-color: black;
        opacity: .5;
        z-index: 5;
    }
</style>