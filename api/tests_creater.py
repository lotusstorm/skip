# coding=utf-8
import os
from collections import namedtuple
from uuid import uuid4
import requests
import inspect
from platform_helpers import import_module
# [IMPORTANT] wmi нужен из за ошибки динамического импорта при использовании методов через REST-Api !!!
import wmi
# ******************
from tc_hub.hg_updater import HubHGUpdater
import sys


PATH = r'D:\Programming\Repositories\axxonnext-auto-testing\test_suites'
sys.path.insert(0, PATH)
CATEGORIES_FILTER = ['blocker', 'major']
SKIPPED_TESTS = ['filter_window']

Module = namedtuple('Module', 'root category component test')


def test_structure(imp_module):
    """

    :return:
    """
    arr = []
    try:
        module_test = import_module('{}.{}'.format('.'.join(imp_module), 'test'))

        for i in inspect.getmembers(module_test):
            if 'Test' in i[0] and inspect.isclass(i[1]):
                data = dict()
                data['class_name'] = i[0]
                data['module_id'] = '.'.join(imp_module)
                data['test_id'] = '{}.{}.{}'.format('.'.join(imp_module), 'test', i[0])
                data['steps'] = []
                for j in inspect.getmembers(i[1]):
                    if ('test' in j[0] or 'step' in j[0]) and inspect.ismethod(j[1]):
                        data['steps'].append({
                            'name': j[0],
                            'description': inspect.getdoc(j[1]),
                            'test_id': '{}.{}.{}'.format('.'.join(imp_module), 'test', i[0]),
                            'step_id': '{}.{}.{}.{}'.format('.'.join(imp_module), 'test',  i[0], j[0])
                        })

                arr.append(data)

        return arr
        # print arr
    except Exception as ex:
        print '{} [ERROR] {}'.format(imp_module, ex)
        return arr

# TODO добавить в структуру теста class_name, поменять название файла type и перенести туда TEST_ID


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
                                'module_id': '.'.join(module),
                                'structures': test_structure(module)
                            }

                    components[test_component] = test_cases
            categories[test_category] = components
    return categories

# print requests.get('http://localhost:5000/api/tests').json()


# print json.dumps(tests_creater(PATH))


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


# add_uuid(PATH)


def update_tests():
    """

    :return:
    """
    pass


def push_tests():
    """
    todo формировать ответ без занесения в bd

    # TODO добавить в структуру теста class_name, поменять название файла type и перенести туда TEST_ID

    :return:
    """
    # a = tests_creater(PATH)
    a = {'branch': 'development'}
    requests.post('http://localhost:5000/api/global_requests', a)
    pass



# HubHGUpdater.pull_and_update_to_head(branch='an-minor')


# push_tests()

# print tests_creater(PATH)

# with open(os.path.join(path, test_category, test_component, test, 'test.py'), 'r') as inp:
#     s = re.compile(r'def ((test|step)_.+?)\(')
#     a = re.findall(s, inp.read())

# a = __import__('test_suites.blocker.0-Ipwizard.test_create_camera.test')

# import_from_module()


# MODULE = 'test_suites.blocker.0-Ipwizard.test_create_camera.test'
# MODULE = 'test_suites.blocker.0-Ipwizard.test_create_camera'
# MODULE = ['test_suites', 'blocker', '05-Archive-mode', 'checking_live_video']
# MODULE = r'test_suites.major.alarms.filter_window'
# print test_structure(MODULE)
