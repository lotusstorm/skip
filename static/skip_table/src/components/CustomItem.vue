<template>
    <li class="custom-item">
        <div
                :class="['table__content-item', modifier, category, active]"
        >
            <app-custom-button
                    :id="id"
                    v-show="isFolder"
                    :modifier="'collapse-button'"
                    @event="collapse(data)"
            ></app-custom-button>
            <h1
                    class="description"
                    @click="selectedConf"
                    :title="description"
            >{{ data.name | validName }}</h1>
            <input
                    type="checkbox"
                    :id="data.current_id"
                    @change="checkElement"
                    :checked="data.skip"
            >
            <label
                    :for="data.current_id"
                    class="checkbox"
            ></label>


        </div>
        <ul :class="['children-wrapper', {'disable' : data.disable}]" v-show="data.collapse">
            <custom-item
                    v-for="(child, index) in data.data"
                    :key="index"
                    :data="child"
                    :id="index"
                    :category="'component'"
                    :description="child.description !== undefined ? child.description : child.name"
                    :modifier="'step--style'"
                    :active="'item--active'"
            ></custom-item>
        </ul>
    </li>
</template>

<script>
    import { mapActions } from 'vuex'
    import { binder, removeClass } from '../store/globalSettings'
    import CustomButton from '@/components/CustomButton.vue'

    export default {
        name: "CustomItem",
        components: {
            'app-custom-button': CustomButton,
        },
        props: {
            'data': Object,
            'id': Number,
            'category': String,
            'description': String,
            'modifier': String,
            'active': String,
        },
        filters: {
            /**
             * Вадидация стоки
             * @param value - строка
             * @returns {string}
             */
            validName(value) {
                value = value.replace(/[-_]/gi, ' ');
                return  value.length >= 25 ? `${value.slice(0, 20)}...` : value;
            }
        },
        computed: {
            isFolder() {
                return this.data.data && this.data.data.length;
            },
        },
        methods: {
            ...mapActions([
                'loadSelected',
            ]),
            /**
             * Групирующий метод для привязки и отвязки issue к выбранному объекту
             * @param event
             */
            checkElement(event) {
                binder(this.data, this.data['issues'], event.target.checked);
                this.selectedConf(event);
                if (!event.target.checked) {
                    this.data['issues'] = []
                }
            },
            /**
             * При выборе объекта конфигурирует нужные елементы для правильной отрисовки
             */
            selectedConf(event) {
                let select = {
                    id:  this.data['current_id'],
                    status: this.data['skip'],
                    data: this.data
                };
                this.loadSelected(select);
                this.addActiveClass(event);
            },
            /**
             * Метод добавляющий css селектор .active к элементу на странице
             * @param event
             */
            addActiveClass(event) {
                let elements = document.querySelectorAll(`.${this.active}`);
                let collapseButton = event.currentTarget.parentElement.querySelector('.collapse-button')
                let collapseButtons = document.querySelectorAll('.collapse-button');

                removeClass(elements, 'active');

                collapseButtons.forEach(el => {
                    el.classList.remove('collapse-button-active');
                });

                if (collapseButton !== null) {
                    collapseButton.classList.add('collapse-button-active');
                }

                event.currentTarget.parentElement.classList.add('active');
            },
            collapse(data) {
                data['collapse'] = !data['collapse'];
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
        margin-left: 10px;
        background-color: var(--items-list-bg-color);
    }

    .custom-item {
        display: flex;
        flex-direction: column;
        width: 100%;
    }

    .custom-item__wrapper {
        display: flex;
        flex-flow: row;
    }

    .checkbox {
        color: #f0f0f0;
        margin: 5px;
    }

</style>