# -*- coding: utf-8 -*-
import os
import sys
from collections import namedtuple
from uuid import uuid4
import inspect
from platform_helpers import import_module
if os.name == 'nt':
    # [IMPORTANT] wmi нужен из за ошибки динамического импорта при использовании методов через REST-Api !!!
    import wmi
    # ******************


PATH = os.path.join(os.environ['AUTOTEST_ROOT_DIR'], 'test_suites')
sys.path.append(PATH)
CATEGORIES_FILTER = ['blocker', 'major']
SKIPPED_TESTS = ['filter_window']

Module = namedtuple('Module', 'root category component test')


def test_structure(imp_module):
    """

    :return:
    """
    arr = []
    try:
        module_test = import_module(_concat([imp_module, 'test']))

        for i in inspect.getmembers(module_test):
            if 'Test' in i[0] and inspect.isclass(i[1]):
                data = {
                    'name': i[0],
                    'module_id': _concat(['test_suites', imp_module]),
                    'id': _concat(['test_suites', imp_module, i[0]]),
                    'data': [],
                }

                for j in inspect.getmembers(i[1]):
                    if ('test' in j[0] or 'step' in j[0]) and inspect.ismethod(j[1]):
                        data['data'].append({
                            'name': j[0],
                            'description': inspect.getdoc(j[1]),
                            'test_id': _concat(['test_suites', imp_module, i[0]]),
                            'id': _concat(['test_suites', imp_module, i[0], j[0]])
                        })

                arr.append(data)

        return arr
        # print arr
    except Exception as ex:
        print '{} [ERROR] {}'.format(imp_module, ex)
        return arr


def _concat(args):
    """

    :param args:
    :return:
    """
    return '.'.join([str(i) if not isinstance(i, list) else _concat(i) for i in args])


def get_test_uuid(imp_module):
    """

    :param imp_module:
    :return:
    """
    module = import_module('{}.{}'.format(imp_module, '__init__'))
    try:
        return module.TEST_ID
    except Exception as ex:
        raise ex


def tests_creater(path):
    """

    :param path:
    :return:
    """
    categories = dict()
    test_categories = os.listdir(path)
    for test_category in test_categories:
        if os.path.isdir(os.path.join(path, test_category)) and test_category in CATEGORIES_FILTER:
            components = dict()
            test_components = os.listdir(os.path.join(path, test_category))
            for test_component in test_components:
                if os.path.isdir(os.path.join(path, test_category, test_component)):
                    test_cases = dict()
                    tests_names = os.listdir(os.path.join(path, test_category, test_component))
                    for test in tests_names:
                        if os.path.isdir(os.path.join(path, test_category, test_component, test)) \
                                and os.listdir(os.path.join(path, test_category, test_component, test)):

                            module = [test_category, test_component, test]
                            test_cases[test] = {
                                'id': _concat(['test_suites', module]),
                                'name': test,
                                'data': test_structure(module),
                            }

                    components[test_component] = {
                        'id': _concat([test_category, test_component]),
                        'name': test_component,
                        'data': test_cases,
                    }
            categories[test_category] = {
                'id': test_category,
                'name': test_category,
                'data': components,
            }
    return categories

def add_uuid(path):
    """

    :param path:
    :return:
    """
    test_categories = os.listdir(path)
    for test_category in test_categories:
        if os.path.isdir(os.path.join(path, test_category)) and test_category in CATEGORIES_FILTER:
            test_components = os.listdir(os.path.join(path, test_category))
            for test_component in test_components:
                if os.path.isdir(os.path.join(path, test_category, test_component)):
                    tests_names = os.listdir(os.path.join(path, test_category, test_component))
                    for test in tests_names:
                        if os.path.isdir(os.path.join(path, test_category, test_component, test)) \
                                and os.listdir(os.path.join(path, test_category, test_component, test)):

                            try:
                                get_test_uuid('.'.join([test_category, test_component, test]))
                            except:
                                with open(os.path.join(path, test_category, test_component, test, '__init__.py'), 'a+') as inp:
                                    inp.write('\nTEST_ID = "{}"\n'.format(uuid4()))
