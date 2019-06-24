<template>
    <li
            @click="addActiveClass"
            class="item module"
    >
        <div
                class="description"
                @click="selectedConf"
                :title="description"
        >{{ name | validName }}</div>
    </li>
</template>

<script>
    import { mapActions } from 'vuex'

    export default {
        name: "ModuleItem",
        props: [
            'name',
            'id',
            'category',
            'data',
            'description',
        ],
        filters: {
            validName(name) {
                return  name.length >= 25 ? `${name.slice(0, 20)}...` : name;
            }
        },
        methods: {
            ...mapActions([
                'loadModuleCategory',
                'loadTestCategory',
                'loadStepCategory',
                'loadSelected',
            ]),
            selectedConf() {
                let data = {
                    id: this.id,
                };

                let data_2 = {
                    id: null,
                    status: false
                };

                this.loadModuleCategory(data);
                this.loadTestCategory(data_2);
                this.loadStepCategory(data_2);
            },
            addActiveClass(event) {
                let element = document.querySelectorAll(`.${this.category.name}`);
                element.forEach(el => {
                    el.classList.remove('active');
                });
                event.currentTarget.classList.add('active');
            },
        }
    }
</script>

<style scoped>
    .module {
        width: 75%;
    }

    .module:hover {
        width: 77%;
    }
</style>