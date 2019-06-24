<template>
    <div class="db-controllers">
        <div class="db-controllers__wrapper">
            <slot></slot>
        </div>
    </div>
</template>

<script>
    export default {
        name: "DbControllers"
    }
</script>

<style>
    .db-controllers {
        display: flex;
        justify-content: center;
    }

    .db-controllers__wrapper {
        display: flex;
        flex-flow: row;
        justify-content: space-around;
        align-items: center;
        height: 50px;
        width: 100%;
    }
</style>