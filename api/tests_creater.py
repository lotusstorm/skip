# -*- coding: utf-8 -*-
import os
import re
import sys
from collections import namedtuple
from platform_helpers import import_module
import inspect

from service_to_synchronize_tests_and_bugs.api.skip_loger import SkipLogger

if os.name == 'nt':
    # [IMPORTANT] wmi нужен из за ошибки динамического импорта при использовании методов через REST-Api !!!
    import wmi
    # ******************
logger = SkipLogger


def test_structure(imp_module, parent_id):
    """
    Преобразует структуру теста в list(dict())
    """
    store = []
    try:
        id_ = path_to_id(os.path.join(imp_module, 'test'))
        module_test = import_module(id_)

        for i in inspect.getmembers(module_test):
            if 'Test' in i[0] and inspect.isclass(i[1]):
                store.append({
                    'name': i[0],
                    'parent_id': parent_id,
                    'current_id': _concat([path_to_id(imp_module), i[0]]),
                    'data': [
                        {
                            'name': j[0],
                            'description': inspect.getdoc(j[1]),
                            'parent_id': _concat([path_to_id(imp_module), i[0]]),
                            'current_id': _concat([path_to_id(imp_module), i[0], j[0]]),
                        } for j in inspect.getmembers(i[1]) if ('test' in j[0] or 'step' in j[0]) and inspect.ismethod(j[1])],
                })

    except Exception as ex:
        logger.exception('{} [ERROR] {}'.format(imp_module, ex))
    return store


def _concat(args):
    """
    Соединяет переданные елементы в id
    """
    return '.'.join([str(i) if not isinstance(i, list) else _concat(i) for i in args])


def path_to_id(path):
    """
    превращает путь в id
    """
    return re.compile(r'test_suites.*').search(path).group(0).replace('\\', '.').replace('/', '.')


def tests_creater(path, parent_id=None, file_name='test'):
    """
    Переводит структуру файловой системы в object
    """
    store_ = []
    listdir_ = os.listdir(path)

    for dir_ in listdir_:
        next_ = os.path.join(path, dir_)
        if os.path.isdir(next_) and '{}.py'.format(file_name) in os.listdir(next_):

            store_.append({
                'parent_id': parent_id,
                'current_id': path_to_id(next_),
                'name': dir_,
                'data': test_structure(next_, parent_id),
            })
            # return store_

        elif os.path.isdir(next_):
            id_ = path_to_id(next_)

            store_.append({
                'parent_id': parent_id,
                'current_id': id_,
                'name': dir_,
                'data': tests_creater(next_, id_, file_name)
            })
    return store_


if __name__ == '__main__':
    from os import walk

    # f = []
    # for (dirpath, dirnames, filenames) in walk(PATH):
    #     f.extend(filenames)
    #     break
    # print f

    # for root, dirs, files in os.walk(PATH):
    #     print (root, os.walk(root).next()[-1])

    # MODULE = ['test_suites', 'internal', 'test_install', 'camera_markers']
    # # MODULE = r'test_suites.major.alarms.filter_window'
    # print test_structure('D:\\Programming\\Repositories\\axxonnext-auto-testing\\test_suites_2\web\helpers_2\\AWS\\test')
    # tests_creater(PATH)
    # test_creater_walk(PATH)
    PATH = os.path.join(os.environ['AUTOTEST_ROOT_DIR'], 'test_suites')
    a = tests_creater(PATH)
    # path_to_id()
    # p = 'D:\\Programming\\Repositories\\axxonnext-auto-testing\\test_suites\\blocker\\14-time-compressor'
    # p = 'D:\\Programming\\Repositories\\axxonnext-auto-testing\\test_suites_2\\web\\helpers_2\\AWS\\test\\TestArchiveSelect'
    # path_to_id(p)
    pass


