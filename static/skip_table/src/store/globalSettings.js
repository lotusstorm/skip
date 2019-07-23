import axios from 'axios/index'


/**
 * Сокращение для того что бы каждый раз не писать адрес и порт сервера
 * @type {AxiosInstance}
 */
export const HTTP = axios.create({
    baseURL: "http://172.17.207.216:5000/api/"
});


/**
 * Точки входа на иерархию ниже в дереве
 * @type {string[]}
 */
export const TREE = ['components', 'modules', 'tests', 'steps'];


/**
 * Рекурсивная функция для модифицирования полученного с сервера массива
 * добавляет во все уровни иерархии новое поле <disable> которое используется для отривоки елементов
 * @param {Array} data - массив
 */
export const distributor = (data) => {

    data = Array.isArray(data) ? data : [data];

    data.forEach(el => {
        el['disable'] = false;
        for (let i in el) {
            if (TREE.indexOf(i) !== -1) {
                distributor(el[i]);
            }
        }
        if (el['skip']) {
            el['disable'] = true
        }
    });
};


/**
 * Глобальная функция для поиска элемента в одномерном массиве
 * @param {Array} data - массив в котором производится поиск
 * @param {String} value - критерый поиска
 * @returns {*} отфильтрованный массив
 */
export const searchIssue = (data, value) => {
    return data.filter((el) => el['name'].toLowerCase().indexOf(value.toLowerCase()) !== -1)
};


/**
 * Рекурсивная функция для обновления привязанных issues у выбранного объекта
 */
export const updater = (data, id) => {
    data = Array.isArray(data) ? data : [data];

    data.forEach(el => {
        for (let i in el) {
            if (TREE.indexOf(i) !== -1) {
                updater(el[i], id);
            }
        }
        el['issues'] = el['issues'].filter(x => x !== id);
    })
};
