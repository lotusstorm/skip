<template>
    <li >
        <input
                type="checkbox"
                :id="id"
                :checked="checked"
                @change="checkElement"
        >
        <label
                :for="id"
                class="checkbox"
                :title="data.description"
        >{{ data.name }} <span class="bug-status">{{ data.status }}</span>
        </label>
        <slot></slot>
    </li>
</template>

<script>
    import { mapGetters } from 'vuex'

    export default {
        name: "Bug",
        props: {
            'id': Number,
            'checked': Boolean,
            'data': Object,
        },
        computed: {
            ...mapGetters([
                'getTests',
                'getSteps',
                'getBugs',
                'getSelected',
            ])
        },
        methods: {
            checkElement(event) {
                let el;
                if (this.getSelected['name'] === 'test') {
                    el = this.getTests.find(el => el['test_id'] === this.getSelected['id']);
                } else {
                    el = this.getSteps.find(el => el['step_id'] === this.getSelected['id']);
                }
                this.addDel(el, event.target.checked, this.id);
            },
            addDel(data, status, id){
                if (status) {
                    if (data['bugs'].indexOf(id) === -1) {
                        data['bugs'].push(id);
                    }
                } else {
                    data['bugs'].splice(data['bugs'].indexOf(id), 1);
                }
            },
        }
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
        margin-right: 30px;
    }
</style>