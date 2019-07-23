# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import (record_info, STRUCTURES, SCHEMAS, USERNAME,
                                                                       PASSWORD, StatusesDeny, search_issue_by_id,
                                                                       issue_repr, serializer)
from service_to_synchronize_tests_and_bugs.api.Structures import db, BugStructure


class TestUpdate(Resource):

    @record_info
    def post(self):
        """

        :return:
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']
        os = json_data['os']
        id_ = json_data['id']

        if os not in STRUCTURES.keys() or os not in SCHEMAS.keys():
            return {'status': 'OS->{} is not supported'.format(os)}, 400

        if branch not in STRUCTURES[os].keys() or branch not in SCHEMAS[os].keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        issues = []

        category_t = STRUCTURES[os][branch]['test_structure'].query.filter_by(test_id=id_).first()
        if not category_t:
            return {'status': 'Category does not exist'}, 400

        if category_t.skip:
            all_issues = category_t.issues

            for i in all_issues:
                issues.append(search_issue_by_id(i, username=USERNAME, password=PASSWORD))

            for issue in set(issues):
                category = BugStructure.query.get(issue.id)

                if category:
                    if issue.fields.status.name in set([i.value for i in StatusesDeny]):

                        if int(issue.id) in category_t.issues:
                            category_t.issues = [i for i in category_t.issues if i != int(issue.id)]
                            if not category_t.issues:
                                category_t.skip = False

                        category_s = STRUCTURES[os][branch]['step_structure'].query.filter_by(test_id=id_).all()
                        if category_s:
                            for step in set(category_s):
                                if int(issue.id) in step.issues:
                                    step.issues = [i for i in step.issues if i != int(issue.id)]
                                    if not step.issues:
                                        step.skip = False

                    category.name = issue.key
                    category.status = issue.fields.status.name
                    category.summary = issue.fields.summary
        else:
            all_issues = []
            category_s = STRUCTURES[os][branch]['step_structure'].query.filter_by(test_id=id_).all()

            if category_s:
                for step in set(category_s):
                    if step.skip:
                        all_issues += step.issues

                for j in all_issues:
                    issues.append(search_issue_by_id(j, username=USERNAME, password=PASSWORD))

                for issue in set(issues):
                    category = BugStructure.query.get(issue.id)

                    if category:
                        if issue.fields.status.name in set([i.value for i in StatusesDeny]):
                            for step in set(category_s):
                                if int(issue.id) in step.issues:
                                    step.issues = [i for i in step.issues if i != int(issue.id)]
                                    if not step.issues:
                                        step.skip = False

                        category.name = issue.key
                        category.status = issue.fields.status.name
                        category.summary = issue.fields.summary

        db.session.commit()

        category_t = STRUCTURES[os][branch]['test_structure'].query.filter_by(test_id=id_).first()
        if not category_t:
            return {'status': 'Category does not exist'}, 400

        data_t, errors_t = SCHEMAS[os][branch]['test_schema'].dump(category_t)
        if errors_t:
            return {"status": "error", "data": errors_t}, 422

        category_s = STRUCTURES[os][branch]['step_structure'].query.filter_by(test_id=id_).all()
        if not category_s:
            return {'status': 'Category does not exist'}, 400

        data_s, errors_s = SCHEMAS[os][branch]['steps_schema'].dump(category_s)
        if errors_s:
            return {"status": "error", "data": errors_s}, 422

        for el in data_s:
            el['issues'] = issue_repr(el)

        data_t['steps'] = data_s
        data_t['issues'] = issue_repr(data_t)

        return {"status": "success", "branch": branch, "data": data_t}, 200


class Tests(Resource):

    @record_info
    def post(self):
        """

        :return:
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']
        os = json_data['os']

        if os not in STRUCTURES.keys() or os not in SCHEMAS.keys():
            return {'status': 'OS->{} is not supported'.format(os)}, 400

        if branch not in STRUCTURES[os].keys() or branch not in SCHEMAS[os].keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[os][branch]['test_structure'].query.all()
        data, errors = SCHEMAS[os][branch]['tests_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": "success", "branch": branch, "data": serializer(os, branch, data)}, 200

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

        if not isinstance(json_data, list):
            json_data = [json_data]

        for data in json_data:
            category = STRUCTURES[os][branch]['test_structure'].query.filter_by(test_id=data['test_id']).first()

            if category:
                category.skip = data['skip']
                category.issues = data['issues']
                category.steps = data['steps']
                category.name = data['name']

        db.session.commit()

        category = STRUCTURES[os][branch]['test_structure'].query.all()
        data, errors = SCHEMAS[os][branch]['tests_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": 'success', "branch": branch, 'data': serializer(os, branch, data)}, 200
