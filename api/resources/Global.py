# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import (record_info, clean_db, STRUCTURES, SCHEMAS,
                                                                       Structure)
from service_to_synchronize_tests_and_bugs.api.Structures import db
from service_to_synchronize_tests_and_bugs.api.tests_creater import tests_creater, PATH
from tc_hub.hg_updater import HubHGUpdater


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

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        # HubHGUpdater.pull_and_update_to_head(branch=branch)
        json_data = tests_creater(PATH)

        if not json_data:
            return {'status': 'No input data provided'}, 400

        for categories in json_data.keys():
            for components in json_data[categories].keys():
                for test_case in json_data[categories][components].keys():

                    module_category = STRUCTURES[branch]['module_structure'](
                        name=test_case,
                        categories=categories,
                        components=components,
                        module_id=json_data[categories][components][test_case]['module_id']
                    )
                    db.session.add(module_category)

                    if json_data[categories][components][test_case]['structures'] is not None:
                        for structure in json_data[categories][components][test_case]['structures']:
                            test_category = STRUCTURES[branch]['test_structure'](
                                name=structure['class_name'],
                                skip=False,
                                test_id=structure['test_id'],
                                module_id=structure['module_id'],
                            )
                            db.session.add(test_category)

                            for step in structure['steps']:
                                step_category = STRUCTURES[branch]['step_structure'](
                                    name=step['name'].decode('utf8'),
                                    skip=False,
                                    test_id=step['test_id'].decode('utf8'),
                                    step_id=step['step_id'].decode('utf8'),
                                    description=step['description'].decode('utf8') if step['description'] is not None else ''
                                )
                                db.session.add(step_category)
        db.session.commit()

        category_t = STRUCTURES[branch]['test_structure'].query.all()
        data_t, errors_t = SCHEMAS[branch]['tests_schema'].dump(category_t)
        if errors_t:
            return {"status": "error", "data": errors_t}, 422

        category_s = STRUCTURES[branch]['step_structure'].query.all()
        data_s, errors_s = SCHEMAS[branch]['steps_schema'].dump(category_s)
        if errors_s:
            return {"status": "error", "data": errors_s}, 422

        category_m = STRUCTURES[branch]['module_structure'].query.all()
        data_m, errors_m = SCHEMAS[branch]['modules_schema'].dump(category_m)
        if errors_m:
            return {"status": "error", "data": errors_m}, 422

        return {"status": 'success', 'tests': data_t, 'steps': data_s, 'modules': data_m}, 200

    @record_info
    def put(self):
        """

        :return:
        """
        req = request.get_json(force=True)
        if not req:
            return {'status': 'No input data provided'}, 400

        branch = req['branch']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        # HubHGUpdater.pull_and_update_to_head(branch=branch)
        json_data = tests_creater(PATH)

        if not json_data:
            return {'status': 'No input data provided'}, 400

        data_categories = json_data.keys()
        categories_for_delete = STRUCTURES[branch]['module_structure'].query.all()
        for el in set(categories_for_delete):
            if el.categories not in data_categories:
                db.session.delete(el)
                all_tests = STRUCTURES[branch]['test_structure'].query.filter_by(module_id=el.module_id).all()
                for test in set(all_tests):
                    db.session.delete(test)

                    all_steps = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=test.test_id).all()
                    for step in set(all_steps):
                        db.session.delete(step)

        for categories in set(data_categories):
            data_components = json_data[categories].keys()
            components_for_delete = STRUCTURES[branch]['module_structure'].query.filter_by(categories=categories).all()
            for el in set(components_for_delete):
                if el.components not in set(data_components):
                    db.session.delete(el)
                    all_tests = STRUCTURES[branch]['test_structure'].query.filter_by(module_id=el.module_id).all()
                    for test in set(all_tests):
                        db.session.delete(test)

                        all_steps = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=test.test_id).all()
                        for step in set(all_steps):
                            db.session.delete(step)

            for components in set(data_components):
                data_test_cases = json_data[categories][components].keys()
                test_cases_for_delete = STRUCTURES[branch]['module_structure'].query.filter_by(categories=categories, components=components).all()

                for el in set(test_cases_for_delete):
                    if el.name not in data_test_cases:
                        db.session.delete(el)
                        all_tests = STRUCTURES[branch]['test_structure'].query.filter_by(
                            module_id=el.module_id).all()
                        for test in set(all_tests):
                            db.session.delete(test)

                            all_steps = STRUCTURES[branch]['step_structure'].query.filter_by(
                                test_id=test.test_id).all()
                            for step in set(all_steps):
                                db.session.delete(step)

                for test_case in set(data_test_cases):

                    module_id = json_data[categories][components][test_case]['module_id']
                    category = STRUCTURES[branch]['module_structure'].query.filter_by(module_id=module_id).first()
                    if not category:
                        module_category = STRUCTURES[branch]['module_structure'](
                            name=test_case,
                            categories=categories,
                            components=components,
                            module_id=module_id
                        )
                        db.session.add(module_category)

                    all_tests = STRUCTURES[branch]['test_structure'].query.filter_by(module_id=module_id).all()
                    structures = json_data[categories][components][test_case]['structures']
                    if structures is not None:
                        for i in set(all_tests):
                            if i.test_id not in [x['test_id'] for x in structures]:
                                db.session.delete(i)

                                all_steps = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=i.test_id).all()
                                for j in all_steps:
                                    db.session.delete(j)

                        for structure in structures:
                            category = STRUCTURES[branch]['test_structure'].query.filter_by(test_id=structure['test_id']).first()
                            if not category:
                                test_category = STRUCTURES[branch]['test_structure'](
                                    name=structure['class_name'],
                                    skip=False,
                                    test_id=structure['test_id'],
                                    module_id=structure['module_id'],
                                )
                                db.session.add(test_category)

                            all_steps = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=structure['test_id']).all()
                            for i in set(all_steps):
                                if i.step_id not in [x['step_id'] for x in structure['steps']]:
                                    db.session.delete(i)

                            for step in structure['steps']:

                                category = STRUCTURES[branch]['step_structure'].query.filter_by(step_id=step['step_id']).first()
                                if category:
                                    category.description = step['description'].decode('utf8') if step['description'] is not None else ''
                                else:
                                    step_category = STRUCTURES[branch]['step_structure'](
                                        name=step['name'].decode('utf8'),
                                        skip=False,
                                        test_id=step['test_id'].decode('utf8'),
                                        step_id=step['step_id'].decode('utf8'),
                                        description=step['description'].decode('utf8') if step['description'] is not None else ''
                                    )
                                    db.session.add(step_category)
        db.session.commit()

        category_t = STRUCTURES[branch]['test_structure'].query.all()
        data_t, errors_t = SCHEMAS[branch]['tests_schema'].dump(category_t)
        if errors_t:
            return {"status": "error", "data": errors_t}, 422

        category_s = STRUCTURES[branch]['step_structure'].query.all()
        data_s, errors_s = SCHEMAS[branch]['steps_schema'].dump(category_s)
        if errors_s:
            return {"status": "error", "data": errors_s}, 422

        category_m = STRUCTURES[branch]['module_structure'].query.all()
        data_m, errors_m = SCHEMAS[branch]['modules_schema'].dump(category_m)
        if errors_m:
            return {"status": "error", "data": errors_m}, 422

        return {"status": 'success', 'tests': data_t, 'steps': data_s, 'modules': data_m}, 200

    @record_info
    def delete(self):
        """

        :return:
        """
        req = request.get_json(force=True)
        if not req:
            return {'status': 'No input data provided'}, 400

        branch = req['branch']

        structure = [
            Structure(structure=STRUCTURES[branch]['test_structure'], schema=SCHEMAS[branch]['tests_schema']),
            Structure(structure=STRUCTURES[branch]['step_structure'], schema=SCHEMAS[branch]['steps_schema']),
            Structure(structure=STRUCTURES[branch]['module_structure'], schema=SCHEMAS[branch]['modules_schema']),
        ]

        data = clean_db(structure)
        return {'data': data}, 200
