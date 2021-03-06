# -*- coding: utf-8 -*-
import re

from flask import request
from flask_restful import Resource
import math
from service_to_synchronize_tests_and_bugs.api.Structures import BugStructure, db, AddictionsStructure
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import (search_issue_by_id, PASSWORD, USERNAME,
                                                                       JQL_BUG_STATUS, search_issue_by_name,
                                                                       search_all_issues, JQL_PROJECT_BUG_STATUS,
                                                                       JQL_PROJECT_BUG, Projects, record_info,
                                                                       JQL_BUGS, StatusesDeny, bug_schema, bugs_schema)


class AddIssue(Resource):
    @record_info
    def post(self):
        """
        Запрос для добавления issue
        """
        json_data = request.get_json(force=True)

        if not json_data:
            return {'status': 'No input data provided'}, 400

        reg = re.compile(r'(({})+-\d+)'.format('|'.join([i.value for i in Projects])))
        issues = [i[0] for i in re.findall(reg, json_data['key'])]

        if not issues:
            return {'status': 'invalid input'}, 400

        err = []
        for issue in set(issues):
            el = BugStructure.query.filter_by(name=issue).first()

            if el:
                err.append(issue)

        if err:
            return {"status": "{} already exist".format(', '.join(err))}, 400

        issues_data = search_issue_by_name(','.join(issues))
        categories = []
        data = []

        for issue in set(issues_data):

            category = BugStructure(
                id=issue.id,
                name=issue.key,
                status=issue.fields.status.name,
                summary=issue.fields.summary
            )
            db.session.add(category)
            categories.append(category)
        db.session.commit()
        for category in set(categories):
            el, errors = bug_schema.dump(category)
            if errors:
                return {"status": "error", "data": errors}, 422

            data.append(el)

        return {"status": 'success', 'data': data}, 200


class UpdateIssue(Resource):
    @record_info
    def put(self):
        """
        Запрос для обновления issue
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        issue = search_issue_by_id(json_data['id'], USERNAME, PASSWORD)

        category = BugStructure.query.get(json_data['id'])

        if not category:
            return {'status': 'Category does not exist'}, 400

        if issue.fields.status.name in set([i.value for i in StatusesDeny]):

            elements = AddictionsStructure.query.all()
            if elements:
                for element in set(elements):
                    if int(json_data['id']) in element.issues:
                        element.issues = [i for i in element.issues if i != int(json_data['id'])]

        category.name = issue.key
        category.status = issue.fields.status.name
        category.summary = issue.fields.summary
        db.session.commit()

        data, errors = bug_schema.dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": 'success', 'data': data}, 200


class DeleteIssue(Resource):
    @record_info
    def post(self):
        """
        Запрос для удаления issue
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        category = BugStructure.query.get(json_data['id'])
        if not category:
            return {'status': 'Category does not exist'}, 400

        elements = AddictionsStructure.query.all()
        if elements:
            for element in set(elements):
                if int(json_data['id']) in element.issues:
                    element.issues = [i for i in element.issues if i != int(json_data['id'])]

        data, errors = bug_schema.dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        db.session.delete(category)
        db.session.commit()

        return {"status": 'success', 'data': data}, 200


class GetIssue(Resource):
    @record_info
    def post(self):
        """
        Запрос для получения более полной информации о конкретном issue
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        issue = search_issue_by_id(json_data['id'], USERNAME, PASSWORD)

        data = {
            'name': issue.key,
            'url': issue.self,
            'summary': issue.fields.summary,
            'description': issue.fields.description,
            'statusName': issue.fields.status.name,
            'statusImg': issue.fields.status.iconUrl,
            'reporter': issue.fields.reporter.displayName,
            'priorityName': issue.fields.priority.name,
            'priorityImg': issue.fields.priority.iconUrl,
            'fixVersions': issue.fields.priority.iconUrl
        }

        return {"status": 'success', 'data': data}, 200


class Issues(Resource):

    @record_info
    def get(self):
        """
        Запрос для получения всех issues из БД
        """
        category = BugStructure.query.all()
        data, errors = bugs_schema.dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": "success", "data": data}, 200

    @record_info
    def post(self):
        """
        Запрос для добавления issues в БД
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        projects = json_data['projects']
        statuses = json_data['statuses']

        if not isinstance(json_data['projects'], list):
            projects = [json_data['projects']]

        if not isinstance(json_data['statuses'], list):
            statuses = [json_data['statuses']]

        if projects and statuses:
            jql = JQL_PROJECT_BUG_STATUS.format(projects=', '.join(projects), statuses=', '.join(statuses))
        elif projects:
            jql = JQL_PROJECT_BUG.format(projects=', '.join(projects))
        else:
            jql = JQL_BUG_STATUS.format(statuses=', '.join(statuses))

        issues = search_all_issues(jql, USERNAME, PASSWORD)

        for issue in issues:
            category = BugStructure.query.get(issue.id)
            if not category:
                category = BugStructure(
                    id=issue.id,
                    name=issue.key,
                    status=issue.fields.status.name,
                    summary=issue.fields.summary
                )
                db.session.add(category)
        db.session.commit()

        category = BugStructure.query.all()
        data, errors = bugs_schema.dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": "success", "data": data}, 200

    @record_info
    def delete(self):
        """
        Запрос для удаления всех issues из БД
        """
        category = BugStructure.query.all()

        elements = AddictionsStructure.query.all()
        if elements:
            for element in set(elements):
                if element.issues:
                    element.skip = False
                    element.issues = []

        for el in set(category):
            db.session.delete(el)
        db.session.commit()

        category = BugStructure.query.all()
        data, errors = bugs_schema.dump(category)
        if data:
            return {"status": "db not cleaned"}, 422

        return {'status': 'db cleaned successfully', "data": data}, 200

    @record_info
    def put(self):
        """
        Запрос для обновления всех issues в БД
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        all_issues = json_data['issues']

        if not isinstance(json_data['issues'], list):
            all_issues = [json_data['issues']]

        iter_start = 0
        iter_end = 450
        step = 450

        issues = []

        for i in range(int(math.ceil(float(len(all_issues))/450))):
            jql = JQL_BUGS.format(key=', '.join(all_issues[iter_start: iter_end]))
            iter_start += step
            iter_end += step

            issues += search_all_issues(jql, USERNAME, PASSWORD)

        for issue in set(issues):
            category = BugStructure.query.get(issue.id)

            if category:
                if issue.fields.status.name in set([i.value for i in StatusesDeny]):
                    elements = AddictionsStructure.query.all()
                    if elements:
                        for element in set(elements):
                            if int(issue.id) in element.issues:
                                element.issues = [i for i in element.issues if i != int(issue.id)]

                category.name = issue.key
                category.status = issue.fields.status.name
                category.summary = issue.fields.summary
        db.session.commit()

        category = BugStructure.query.all()
        data, errors = bugs_schema.dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": 'success', 'data': data}, 200
