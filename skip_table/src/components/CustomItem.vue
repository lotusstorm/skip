<template>
    <li  class="custom-item">
        <div
                :class="['item', 'item-modifier', category.name]"
                @click="addActiveClass"
        >
            <input
                    type="checkbox"
                    :id="id"
                    :checked="checked"
                    @change="checkElement"
            >
            <label
                    :for="id"
                    class="checkbox"
            ></label>
            <h1
                    class="description"
                    @click="selectedConf"
                    :title="description"
            >{{ name | validName }}</h1>
        </div>

        <div class="children-wrapper" v-if="!checked && category.name === 'test'">
<!--        <div class="children-wrapper" v-if="category.name === 'test'">-->
            <slot></slot>
        </div>
    </li>
</template>

<script>
    import { mapActions, mapGetters } from 'vuex'

    export default {
        name: "CustomItem",
        props: [
            'checked',
            'name',
            'id',
            'test_id',
            'category',
            'data',
            'description',
        ],
        filters: {
            validName(name) {
                return  name.length >= 25 ? `${name.slice(0, 20)}...` : name;
            }
        },
        computed: {
            ...mapGetters([
                'getSteps',
             ]),
        },
        methods: {
            ...mapActions([
                'loadTestCategory',
                'loadStepCategory',
                'loadSelected',
            ]),
            checkElement(event) {
                let el;

                if (this.category['name'] === 'step') {
                    el = this.data.find((el) => el['step_id'] === this.id);

                    if (!event.target.checked) {
                        el['bugs'] = []
                    }
                } else {
                    el = this.data.find((el) => el['test_id'] === this.id);

                    if (!event.target.checked) {
                        el['bugs'] = [];
                        this.getSteps.forEach(i => {
                            if (i['test_id'] === this.id) {
                                i['skip'] = event.target.checked;
                                i['bugs'] = [];
                            }
                        });
                    } else {
                        this.getSteps.forEach(i => {
                            if (i['test_id'] === this.id) {
                                i['skip'] = event.target.checked;
                                i['bugs'] = el['bugs'];
                            }
                        });
                    }
                }

                el['skip'] = event.target.checked;
                this.selectedConf();
            },
            selectedConf() {
                let data;
                let el;
                if (this.category['name'] === 'step') {
                    el = this.data.find((el) => el['step_id'] === this.id);
                    data = {
                        id: this.id,
                        status: el['skip']
                    };
                    this.loadStepCategory(data);
                } else {
                    el = this.data.find((el) => el['test_id'] === this.id);
                    data = {
                        id: this.id,
                        status: el['skip']
                    };

                    this.loadTestCategory(data);
                }
                this.loadSelected(this.category);
            },
            addActiveClass(event) {
                let element = document.querySelectorAll('.item-modifier');
                element.forEach(el => {
                    el.classList.remove('active');
                });
                event.currentTarget.classList.add('active');
            },
        }
    }
</script>

<style scoped>
    .children-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        width: 95%;
        margin-top: 5px;
        margin-left: 10px;
        background-color: var(--items-list-bg-color);
    }

    .custom-item {
        display: flex;
        flex-direction: column;
        width: 100%;
    }

</style>