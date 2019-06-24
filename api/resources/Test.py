# -*- coding: utf-8 -*-
import math

from flask import request
from flask_restful import Resource
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import record_info, STRUCTURES, SCHEMAS, JQL_BUGS, \
    search_all_issues, USERNAME, PASSWORD, StatusesDeny, search_issue_by_id
from service_to_synchronize_tests_and_bugs.api.Structures import db, BugStructure


class TestUpdate(Resource):
    # @record_info
    # def post(self):
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'status': 'No input data provided'}, 400
    #
    #     all_issues = json_data['issues']
    #     branch = json_data['branch']
    #     id_ = json_data['id']
    #
    #     if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
    #         return {'status': 'Branch->{} is not supported'.format(branch)}, 400
    #
    #     if not isinstance(json_data['issues'], list):
    #         all_issues = [json_data['issues']]
    #
    #     iter_start = 0
    #     iter_end = 450
    #     step = 450
    #
    #     issues = []
    #
    #     for i in range(int(math.ceil(float(len(set(all_issues))) / 450))):
    #         jql = JQL_BUGS.format(key=', '.join(all_issues[iter_start: iter_end]))
    #         iter_start += step
    #         iter_end += step
    #
    #         issues += search_all_issues(jql, USERNAME, PASSWORD)
    #
    #     for issue in set(issues):
    #         category = BugStructure.query.get(issue.id)
    #
    #         if category:
    #             if issue.fields.status.name in set([i.value for i in StatusesDeny]):
    #
    #                 category_t = STRUCTURES[branch]['test_structure'].query.filter_by(test_id=id_).first()
    #                 if category_t:
    #                     for test in {category_t}:
    #                         if test.bugs and int(issue.id) in test.bugs:
    #                             test.bugs = [i for i in test.bugs if i != int(issue.id)]
    #                             if not test.bugs:
    #                                 test.skip = False
    #
    #                 category_s = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=id_).all()
    #                 if category_s:
    #                     for step in set(category_s):
    #                         if step.bugs and int(issue.id) in step.bugs:
    #                             step.bugs = [i for i in step.bugs if i != int(issue.id)]
    #                             if not step.bugs:
    #                                 step.skip = False
    #
    #             category.name = issue.key
    #             category.status = issue.fields.status.name
    #             category.description = issue.fields.summary
    #     db.session.commit()
    #
    #     category = STRUCTURES[branch]['test_structure'].query.filter_by(test_id=id_).first()
    #
    #     if not category:
    #         return {'status': 'Category does not exist'}, 400
    #
    #     data, errors = SCHEMAS[branch]['test_schema'].dump(category)
    #     if errors:
    #         return {"status": "error", "data": errors}, 422
    #
    #     arr = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=id_).all()
    #     data['steps'] = SCHEMAS[branch]['steps_schema'].dump(arr).data
    #
    #     return {"status": "success", "data": data}, 200

    @record_info
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        all_issues = json_data['issues']
        branch = json_data['branch']
        id_ = json_data['id']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        if not isinstance(json_data['issues'], list):
            all_issues = [json_data['issues']]

        issues = []

        for i in all_issues:
            issues.append(search_issue_by_id(i, username=USERNAME, password=PASSWORD))

        for issue in set(issues):
            category = BugStructure.query.get(issue.id)

            if category:
                if issue.fields.status.name in set([i.value for i in StatusesDeny]):

                    category_t = STRUCTURES[branch]['test_structure'].query.filter_by(test_id=id_).first()
                    if category_t:
                        for test in {category_t}:
                            if test.bugs and int(issue.id) in test.bugs:
                                test.bugs = [i for i in test.bugs if i != int(issue.id)]
                                if not test.bugs:
                                    test.skip = False

                    category_s = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=id_).all()
                    if category_s:
                        for step in set(category_s):
                            if step.bugs and int(issue.id) in step.bugs:
                                step.bugs = [i for i in step.bugs if i != int(issue.id)]
                                if not step.bugs:
                                    step.skip = False

                category.name = issue.key
                category.status = issue.fields.status.name
                category.description = issue.fields.summary
        db.session.commit()

        category = STRUCTURES[branch]['test_structure'].query.filter_by(test_id=id_).first()

        if not category:
            return {'status': 'Category does not exist'}, 400

        data, errors = SCHEMAS[branch]['test_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        arr = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=id_).all()
        data['steps'] = SCHEMAS[branch]['steps_schema'].dump(arr).data

        return {"status": "success", "data": data}, 200


class Test(Resource):

    @record_info
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']
        id_ = json_data['id']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[branch]['test_structure'].query.filter_by(test_id=id_).first()

        if not category:
            return {'status': 'Category does not exist'}, 400

        data, errors = SCHEMAS[branch]['test_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        arr = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=id_).all()
        data['steps'] = SCHEMAS[branch]['steps_schema'].dump(arr).data

        return {"status": "success", "data": data}, 200


class Tests(Resource):

    @record_info
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[branch]['test_structure'].query.all()
        data, errors = SCHEMAS[branch]['tests_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": "success", "branch": branch, "data": data}, 200

    @record_info
    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']
        json_data = json_data['data']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        if not isinstance(json_data, list):
            json_data = [json_data]

        for data in json_data:
            category = STRUCTURES[branch]['test_structure'].query.filter_by(test_id=data['test_id']).first()

            if category:
                category.skip = data['skip']
                category.bugs = data['bugs']
                category.steps = data['steps']
                category.name = data['name']

        db.session.commit()

        category = STRUCTURES[branch]['test_structure'].query.all()
        data, errors = SCHEMAS[branch]['tests_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": 'success', 'data': data}, 200

    @record_info
    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[branch]['test_structure'].query.all()

        for el in category:
            db.session.delete(el)
        db.session.commit()

        category = STRUCTURES[branch]['test_structure'].query.all()
        data, errors = SCHEMAS[branch]['tests_schema'].dump(category)
        if data:
            return {"status": "db not cleaned"}, 422

        return {'status': 'db cleaned successfully', "data": data}, 200

    # @record_info
    # def post(self):
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'status': 'No input data provided'}, 400
    #
    #     branch = json_data['branch']
    #
    #     if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
    #         return {'status': 'Branch->{} is not supported'.format(branch)}, 400
    #
    #     if not isinstance(json_data, list):
    #         json_data = [json_data['data']]
    #
    #     for data in json_data:
    #         category = STRUCTURES[branch]['test_structure'](
    #             skip=data['skip'],
    #             test_id=data['test_id'],
    #             name=data['name'],
    #             module_id=data['module_id'],
    #         )
    #         db.session.add(category)
    #     db.session.commit()
    #
    #     category = STRUCTURES[branch]['test_structure'].query.all()
    #     data, errors = SCHEMAS[branch]['tests_schema'].dump(category)
    #     if errors:
    #         return {"status": "error", "data": errors}, 422
    #
    #     return {"status": 'success', 'data': data}, 200
