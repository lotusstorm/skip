<template>
    <li class="custom-item">
        <div
                :class="['table__content-item', modifier, category, active]"
        >
            <input
                    type="checkbox"
                    :id="id"
                    @change="checkElement"
                    :checked="data.skip"
            >
            <label
                    :for="id"
                    class="checkbox"
            ></label>
            <h1
                    class="description"
                    @click="selectedConf"
                    :title="description"
            >{{ data.name | validName }}</h1>
            <slot name="controllers"></slot>
        </div>
        <div :class="['children-wrapper', {'disable' : data.disable}]" v-show="data.collapse">
            <slot name="childrens"></slot>
        </div>
    </li>
</template>

<script>
    import { mapActions } from 'vuex'
    import { TREE } from '../store/globalSettings'

    export default {
        name: "CustomItem",
        data() {
            return {
                show: false,
                ignore: ['test', 'step'],
            }
        },
        props: {
            'data': Object,
            'description': String,
            'id': String,
            'category': String,
            'disable': Array,
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
        methods: {
            ...mapActions([
                'loadSelected',
                'loadTestRender',
            ]),
            /**
             * Групирующий метод для привязки и отвязки issue к выбранному объекту
             * @param event
             */
            checkElement(event) {
                this.binder(this.data, this.data['issues'], event.target.checked);
                this.selectedConf();
                if (!event.target.checked) {
                    this.data['issues'] = []
                }
            },
            /**
             * При выборе объекта конфигурирует нужные елементы для правильной отрисовки
             */
            selectedConf() {
                let data = {
                    id:  this.data['id'],
                    status: this.data['skip'],
                    name: this.category,
                    data: this.data
                };

                if (this.category === 'module') {
                    let render = {
                        data: this.data['tests'],
                        disable: !this.data['skip'],
                    };

                    this.loadTestRender(render);
                } else if (this.ignore.indexOf(this.category) === -1) {
                    let render = {
                        data: [],
                    };
                    this.loadTestRender(render);
                }

                this.loadSelected(data);
                this.addActiveClass(event);
            },
            /**
             * Рекурсивная метод для конфигурирования дерева выбранного объекта
             * при активном чек-бокс родителя все дочерние елементы становятся не активными и к их привязанным issues
             * добаляется issues родителя при неактивном все проделявается обратно
             * @param {Array} data - массив объектов по которому надо итерироватся
             * @param {Array} issues - список привязанных элементов который надо добавить или убрать у всех объектов в дереве
             * @param {Boolean} skip - состояние чек-бокса
             */
            binder(data, issues, skip) {
                data = Array.isArray(data) ? data : [data];

                data.forEach(el => {
                    for (let i in el) {
                        if (TREE.indexOf(i) !== -1) {
                            this.binder(el[i], issues, skip);
                        }
                    }
                    if (skip) {
                        el['skip'] = skip;
                        el['issues'] = el['issues'].concat(issues);
                    } else {
                        el['issues'] = el['issues'].filter(x => issues.indexOf(x) === -1);
                        if (el['issues'].length === 0){
                            el['skip'] = skip;
                        }
                    }
                    el['disable'] = el['skip'];
                })
            },
            /**
             * Метод добавляющий css селектор .active к элементу на странице
             * @param event
             */
            addActiveClass(event) {
                let element = document.querySelectorAll(`.${this.active}`);
                let collapseButton = event.currentTarget.parentElement.querySelector('.collapse-button')
                let collapseButtons = document.querySelectorAll('.collapse-button');

                element.forEach(el => {
                    el.classList.remove('active');
                });

                collapseButtons.forEach(el => {
                    el.classList.remove('collapse-button-active');
                });

                if (collapseButton !== null) {
                //     // let styles = getComputedStyle(document.documentElement);
                //     // let colorValue = styles.getPropertyValue(`--${this.category}-style`);
                    
                //     // document.documentElement.style.setProperty ('--collapse-btn-active-color', colorValue);
                    collapseButton.classList.add('collapse-button-active');
                }

                event.currentTarget.parentElement.classList.add('active');
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
    }

</style>