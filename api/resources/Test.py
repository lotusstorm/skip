# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import (record_info, USERNAME, PASSWORD, StatusesDeny,
                                                                       search_issue_by_id, issue_repr, issue_binder,
                                                                       addictions_schema)
from service_to_synchronize_tests_and_bugs.api.Structures import db, BugStructure, AddictionsStructure


class TestUpdate(Resource):

    @record_info
    def post(self):
        """
        Запрос для маниторинга состояния issues при выполнении тестов
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch_ = json_data['branch']
        os_ = json_data['os']
        id_ = json_data['id']

        issues = []
        item = {}

        category_t = AddictionsStructure.query.filter_by(os=os_, branch=branch_, parent_id=id_).all()
        if not category_t:
            return {'status': 'Category does not exist'}, 400

        if category_t:
            for step in set(category_t):

                if step.issues:
                    all_issues = step.issues

                    for i in all_issues:
                        issues.append(search_issue_by_id(i, username=USERNAME, password=PASSWORD))

                    for issue in set(issues):
                        category = BugStructure.query.get(issue.id)

                        if category:
                            if issue.fields.status.name in set([i.value for i in StatusesDeny]):

                                if int(issue.id) in step.issues:
                                    step.issues = [i for i in step.issues if i != int(issue.id)]

                            category.name = issue.key
                            category.status = issue.fields.status.name
                            category.summary = issue.fields.summary

            db.session.commit()

        category_t = AddictionsStructure.query.filter_by(os=os_, branch=branch_, parent_id=id_).all()
        if not category_t:
            return {'status': 'Category does not exist'}, 400
        data, errors_t = addictions_schema.dump(category_t)

        item['skip'] = False
        item['os'] = os_
        item['branch'] = branch_
        item['issues'] = []
        item['data'] = data
        issues = issue_binder([i['issues'] for i in data])
        if issues:
            item['skip'] = True
            item['issues'] = issue_repr(issues)

        for i in data:
            i['issues'] = issue_repr(i['issues'])

        return {"status": "success", "data": item}, 200
