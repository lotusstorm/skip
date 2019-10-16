<template>
    <li :class="modifier">
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
        <div 
                class="issue-content" 
                :title="data.summary" 
                @click="toDescriptions(id)"
        >
            <h1 class="issue-name">{{ data.name }} </h1>
            <span class="issue-status">{{ data.status }}</span>
        </div>
        <slot></slot>
    </li>
</template>

<script>
    import { mapGetters } from 'vuex'
    import { status } from '../store/globalSettings'

    export default {
        name: "Issue",
        props: {
            'id': Number,
            'checked': Boolean,
            'data': Object,
            'modifier': String,
        },
        computed: {
            ...mapGetters([
                'getSelected',
                'getData',
            ])
        },
        methods: {
            /**
             * Объеденяющий метод для выполнения нужных методов
             * @param event
             */
            checkElement(event) {
                this.checker(this.getSelected['data'], event.target.checked, this.id);
                status(this.getData);
                this.getSelected['status'] = this.getSelected['data']['issues'].length !== 0
            },
            /**
             * роутинг
             */
            toDescriptions(id) {
                this.$router.push({name: 'home_description', params: {id}})
            },
            /**
             * Рекурсивный метод для привязывания и отвязывания issue к выбранному объекту
             * @param {Array} data - массив в котором производится поиск
             * @param {Boolean} status - состояние определяет привязать или отвязать issue
             * @param id - issue добаляемый/убираемый при чеке ко всем вложеностям дерева
             */
            checker(data, status, id) {
                data = Array.isArray(data) ? data : [data];

                data.forEach(el => {
                    if (Object.keys(el).indexOf('data') !== -1) {
                        this.checker(el['data'], status, id);
                    }

                    if (status) {
                        if (el['issues'].indexOf(id) === -1) {
                            el['issues'].push(id);
                        }
                    } else {
                        el['issues'] = el['issues'].filter(x => x !== id);
                    }
                });
            },

        }
    }
</script>

<style scoped>
    .issue-content {
        display: flex;
        align-items: center;
        width: 80%;
        height: 40px;
        justify-content: space-between;
    }

    .issue-name {
        margin-left: 10px;
    }

    .issue-status {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        background-color: #2ab192b3;
        color: #f0f0f0;
        padding: 2px 4px;
        font-size: 15px;
        border-radius: 3px;
    }
</style>