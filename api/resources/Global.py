# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from platform_helpers import EcosystemSettings
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import (record_info, clean_db, STRUCTURES,
                                                                       SCHEMAS, Structure, serializer, clean_if_in)
from service_to_synchronize_tests_and_bugs.api.Structures import db
from service_to_synchronize_tests_and_bugs.api.tests_creater import tests_creater, PATH
from mercurial_lib.hg_updater import HGClientWrapper


class GlobalRequests(Resource):

    @record_info
    def post(self):
        """

        :return:
        """
        req = request.get_json(force=True)
        if not req:
            return {'status': 'No input data provided'}, 400

        branch = req['branch']
        os = req['os']

        if os not in STRUCTURES.keys() or os not in SCHEMAS.keys():
            return {'status': 'OS->{} is not supported'.format(os)}, 400

        if branch not in STRUCTURES[os].keys() or branch not in SCHEMAS[os].keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        HGClientWrapper.pull_and_update_to_head(hg_dir=EcosystemSettings.ROOT_DIR,
                                                source="https://vonegosh:Zamolchisvoirot1@bitbucket.org/Axxonsoft/axxonnext_autotests",
                                                branch=branch) #IMPORTANT раскоментить
        json_data = tests_creater(PATH)

        if not json_data:
            return {'status': 'No input data provided'}, 400

        for category in json_data.values():
            el = STRUCTURES[os][branch]['category_structure'].query.filter_by(category_id=category['id']).first()
            if not el:
                module_category = STRUCTURES[os][branch]['category_structure'](
                    name=category['name'],
                    skip=False,
                    category_id=category['id']
                )
                db.session.add(module_category)

            for component in category['data'].values():
                el = STRUCTURES[os][branch]['component_structure'].query.filter_by(component_id=component['id']).first()
                if not el:
                    module_category = STRUCTURES[os][branch]['component_structure'](
                        name=component['name'],
                        skip=False,
                        category_id=category['id'],
                        component_id=component['id']
                    )
                    db.session.add(module_category)

                for module in component['data'].values():
                    el = STRUCTURES[os][branch]['module_structure'].query.filter_by(module_id=module['id']).first()
                    if not el:
                        module_category = STRUCTURES[os][branch]['module_structure'](
                            name=module['name'],
                            component_id=component['id'],
                            skip=False,
                            module_id=module['id']
                        )
                        db.session.add(module_category)

                    if module['data'] is not None:
                        for structure in module['data']:
                            el = STRUCTURES[os][branch]['test_structure'].query.filter_by(test_id=structure['id']).first()
                            if not el:
                                test_category = STRUCTURES[os][branch]['test_structure'](
                                    name=structure['name'],
                                    skip=False,
                                    test_id=structure['id'],
                                    module_id=structure['module_id'],
                                )
                                db.session.add(test_category)

                            for step in structure['data']:
                                el = STRUCTURES[os][branch]['step_structure'].query.filter_by(step_id=step['id']).first()
                                if not el:
                                    step_category = STRUCTURES[os][branch]['step_structure'](
                                        name=step['name'],
                                        skip=False,
                                        test_id=step['test_id'],
                                        step_id=step['id'],
                                        description=step['description'].decode('utf8') if step['description'] is not None else ''
                                    )
                                    db.session.add(step_category)
        db.session.commit()

        category_c = STRUCTURES[os][branch]['category_structure'].query.all()
        data_c, errors_c = SCHEMAS[os][branch]['categories_schema'].dump(category_c)
        if errors_c:
            return {"status": "error", "data": errors_c}, 422

        return {"status": 'success', "branch": branch, 'categories': serializer(os, branch, data_c)}, 200

    @record_info
    def put(self):
        """

        :return:
        """
        req = request.get_json(force=True)
        if not req:
            return {'status': 'No input data provided'}, 400

        branch = req['branch']
        os = req['os']

        if os not in STRUCTURES.keys() or os not in SCHEMAS.keys():
            return {'status': 'OS->{} is not supported'.format(os)}, 400

        if branch not in STRUCTURES[os].keys() or branch not in SCHEMAS[os].keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        HGClientWrapper.pull_and_update_to_head(hg_dir=EcosystemSettings.ROOT_DIR,
                                                source="https://vonegosh:Zamolchisvoirot1@bitbucket.org/Axxonsoft/axxonnext_autotests",
                                                branch=branch) #IMPORTANT раскоментить
        json_data = tests_creater(PATH)

        if not json_data:
            return {'status': 'No input data provided'}, 400

        data_categories = json_data.keys()
        db_categories = STRUCTURES[os][branch]['category_structure'].query.all()
        if db_categories:
            clean_if_in(db_categories, data_categories)

        for category in json_data.values():
            el = STRUCTURES[os][branch]['category_structure'].query.filter_by(category_id=category['id']).first()
            if not el:
                module_category = STRUCTURES[os][branch]['category_structure'](
                    name=category['name'],
                    skip=False,
                    category_id=category['id']
                )
                db.session.add(module_category)

            data_component = category['data'].keys()
            db_component = STRUCTURES[os][branch]['component_structure'].query.filter_by(category_id=category['id']).all()
            if db_component:
                clean_if_in(db_component, data_component)

            for component in category['data'].values():
                el = STRUCTURES[os][branch]['component_structure'].query.filter_by(component_id=component['id']).first()
                if not el:
                    module_category = STRUCTURES[os][branch]['component_structure'](
                        name=component['name'],
                        skip=False,
                        category_id=category['id'],
                        component_id=component['id']
                    )
                    db.session.add(module_category)

                data_module = component['data'].keys()
                db_module = STRUCTURES[os][branch]['module_structure'].query.filter_by(component_id=component['id']).all()
                if db_module:
                    clean_if_in(db_module, data_module)

                for module in component['data'].values():
                    el = STRUCTURES[os][branch]['module_structure'].query.filter_by(module_id=module['id']).first()
                    if not el:
                        module_category = STRUCTURES[os][branch]['module_structure'](
                            name=module['name'],
                            component_id=component['id'],
                            skip=False,
                            module_id=module['id']
                        )
                        db.session.add(module_category)

                    data_test = [i['name'] for i in module['data']]
                    db_test = STRUCTURES[os][branch]['test_structure'].query.filter_by(module_id=module['id']).all()
                    if db_test:
                        clean_if_in(db_test, data_test)

                    if module['data'] is not None:
                        for structure in module['data']:
                            el = STRUCTURES[os][branch]['test_structure'].query.filter_by(test_id=structure['id']).first()
                            if not el:
                                test_category = STRUCTURES[os][branch]['test_structure'](
                                    name=structure['name'],
                                    skip=False,
                                    test_id=structure['id'],
                                    module_id=structure['module_id'],
                                )
                                db.session.add(test_category)

                            data_steps = [i['name'] for i in structure['data']]
                            db_steps = STRUCTURES[os][branch]['step_structure'].query.filter_by(test_id=structure['id']).all()
                            if db_steps:
                                clean_if_in(db_steps, data_steps)

                            for step in structure['data']:
                                el = STRUCTURES[os][branch]['step_structure'].query.filter_by(step_id=step['id']).first()
                                if el:
                                    el.description = step['description'].decode('utf8') if step['description'] is not None else ''
                                else:
                                    step_category = STRUCTURES[os][branch]['step_structure'](
                                        name=step['name'],
                                        skip=False,
                                        test_id=step['test_id'],
                                        step_id=step['id'],
                                        description=step['description'].decode('utf8') if step['description'] is not None else ''
                                    )
                                    db.session.add(step_category)
        db.session.commit()

        category_c = STRUCTURES[os][branch]['category_structure'].query.all()
        data_c, errors_c = SCHEMAS[os][branch]['categories_schema'].dump(category_c)
        if errors_c:
            return {"status": "error", "data": errors_c}, 422

        return {"status": 'success', "branch": branch, 'categories': serializer(os, branch, data_c)}, 200

    @record_info
    def delete(self):
        """

        :return:
        """
        req = request.get_json(force=True)
        if not req:
            return {'status': 'No input data provided'}, 400

        branch = req['branch']
        os = req['os']

        if os not in STRUCTURES.keys() or os not in SCHEMAS.keys():
            return {'status': 'OS->{} is not supported'.format(os)}, 400

        if branch not in STRUCTURES[os].keys() or branch not in SCHEMAS[os].keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        structure = [
            Structure(structure=STRUCTURES[os][branch]['test_structure'], schema=SCHEMAS[os][branch]['tests_schema']),
            Structure(structure=STRUCTURES[os][branch]['step_structure'], schema=SCHEMAS[os][branch]['steps_schema']),
            Structure(structure=STRUCTURES[os][branch]['module_structure'], schema=SCHEMAS[os][branch]['modules_schema']),
        ]

        data = clean_db(structure)
        return {"branch": branch, 'data': data}, 200


class GlobalUpdate(Resource):

    @record_info
    def put(self):
        """

        :return:
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']
        os = json_data['os']
        json_data = json_data['data']

        if os not in STRUCTURES.keys() or os not in SCHEMAS.keys():
            return {'status': 'OS->{} is not supported'.format(os)}, 400

        if branch not in STRUCTURES[os].keys() or branch not in SCHEMAS[os].keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        # updater(branch=branch, data=json_data) #IMPORTANT ДОДЕЛАТЬ РЕКУРСИЮ
        for category in json_data:
            el = STRUCTURES[os][branch]['category_structure'].query.filter_by(category_id=category['category_id']).first()
            if el:
                el.skip = category['skip']
                el.issues = category['issues']

            for component in category['components']:
                el = STRUCTURES[os][branch]['component_structure'].query.filter_by(component_id=component['component_id']).first()
                if el:
                    el.skip = component['skip']
                    el.issues = component['issues']

                for module in component['modules']:
                    el = STRUCTURES[os][branch]['module_structure'].query.filter_by(module_id=module['module_id']).first()
                    if el:
                        el.skip = module['skip']
                        el.issues = module['issues']

                    for test in module['tests']:
                        el = STRUCTURES[os][branch]['test_structure'].query.filter_by(test_id=test['test_id']).first()
                        if el:
                            el.skip = test['skip']
                            el.issues = test['issues']

                        for step in test['steps']:
                            el = STRUCTURES[os][branch]['step_structure'].query.filter_by(step_id=step['step_id']).first()
                            if el:
                                el.skip = step['skip']
                                el.issues = step['issues']
        db.session.commit()

        category_c = STRUCTURES[os][branch]['category_structure'].query.all()
        data_c, errors_c = SCHEMAS[os][branch]['categories_schema'].dump(category_c)
        if errors_c:
            return {"status": "error", "data": errors_c}, 422

        return {"status": 'success', "branch": branch, 'categories': serializer(os, branch, data_c)}, 200
