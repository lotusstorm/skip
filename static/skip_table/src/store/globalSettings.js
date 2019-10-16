import axios from 'axios/index'


/**
 * Сокращение для того что бы каждый раз не писать адрес и порт сервера
 * @type {AxiosInstance}
 */
export const HTTP = axios.create({
    baseURL: "http://localhost:5000/api/"
});

export const HTTP_2 = axios.create({
    baseURL: "http://localhost:5000/api/",
    responseType: 'blob',
});


/**
 * Рекурсивная функция для модифицирования полученного с сервера массива
 * добавляет во все уровни иерархии новое поле <disable> которое используется для отрисовки елементов
 * @param {Array} new_data - массив
 * @param old_data
 * @param cache
 */
export const distributor = (new_data, old_data, cache=false) => {
    new_data = Array.isArray(new_data) ? new_data : [new_data];

    new_data.forEach(el => {
        if (Object.keys(el).indexOf('data') !== -1) {
            distributor(el['data'], old_data, cache);
        }

        el['disable'] = el['skip'];

        if (cache && old_data.length !== 0) {
            equal(old_data, el)
        } else {
            el['collapse'] = false;
        }
    });
};

const equal = (old_data, new_data_el) => {

    old_data = Array.isArray(old_data) ? old_data : [old_data];

    for (let el of old_data) {

        if (el['current_id'] === new_data_el['current_id']) {
            new_data_el['collapse'] = el['collapse'];
            break
        }
        if (Object.keys(el).indexOf('data') !== -1) {
            equal(el['data'], new_data_el);
        }

    }
};


export const removeClass = (elements, removed_class) => {
    elements.forEach(el => {
        el.classList.remove(removed_class);
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
        if (Object.keys(el).indexOf('data') !== -1) {
            updater(el['data'], id);
        }

        el['issues'] = el['issues'].filter(x => x !== id);
    })
};


/**
 * Сохраняет в localstore координаты скрола
 * @param {*} event 
 */
export const scroll = (event) => {
    localStorage.setItem(`${event.target.id}`, event.target.scrollTop);
};


/**
 * Рекурсивная метод для конфигурирования дерева выбранного объекта
 * при активном чек-бокс родителя все дочерние елементы становятся не активными и к их привязанным issues
 * добаляется issues родителя при неактивном все проделявается обратно
 * @param {Array} data - массив объектов по которому надо итерироватся
 * @param {Array} issues - список привязанных элементов который надо добавить или убрать у всех объектов в дереве
 * @param {Boolean} skip - состояние чек-бокса
 */
export const binder = (data, issues, skip) => {
    data = Array.isArray(data) ? data : [data];

    data.forEach(el => {
        if (Object.keys(el).indexOf('data') !== -1) {
            binder(el['data'], issues, skip);
        }
        if (skip) {
            el['skip'] = skip;
            el['issues'] = el['issues'].concat(issues);
        } else {
            el['issues'] = el['issues'].filter(x => issues.indexOf(x) === -1);
            if (el['issues'].length === 0) {
                el['skip'] = skip;
            }
        }

        el['disable'] = el['skip'];
    })
};


/**
 *
 *
 * */
export const status = (data) => {
    data = Array.isArray(data) ? data : [data];

    data.forEach(el => {
        if (Object.keys(el).indexOf('data') !== -1) {
            status(el['data']);

            el['skip'] = false;
            el['issues'] = [];
            el['disable'] = false;

            let issues = el['data'].map(a => a['issues']);
            if (issueBinder(issues).length !== 0) {
                el['skip'] = true;
                el['issues'] = issueBinder(issues);
                el['disable'] = true;
            }
        } else {
            el['skip'] = el['issues'].length !== 0;
        }
    });
};

/**
 *
 * */
const issueBinder = (data) => {
    let a = [];
    data.forEach(f => a.push(...f));

    let b = new Set(a);
    let arr = [];
    b.forEach(f => {
        if (a.filter(item => item === f).length === data.length) {
            arr.push(f)
        }

    });
    return arr
};
