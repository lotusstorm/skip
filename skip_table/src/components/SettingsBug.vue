<template>
    <li >
        <div
                :id="id"
                class="checkbox"
        >{{ data.name }}
            <span class="bug-status">{{ data.status }}</span>
        </div>
        <slot></slot>
    </li>
</template>

<script>
    export default {
        name: "Bug",
        props: {
            'checked': Boolean,
            'data': Object,
            'id': Number,
        },
    }

</script>

<style scoped>
    .checkbox {
        display: flex;
        flex-grow: 1;
        margin-left: 10px;
        cursor: pointer;
        height: 35px;
        align-items: center;
        justify-content: space-between;
    }

    .bug-status {
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