# -*- coding: utf-8 -*-
import re

from flask import request
from flask_restful import Resource
import math
from service_to_synchronize_tests_and_bugs.api.Structures import BugSchema, BugStructure, db
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import (search_issue_by_id,
                                                                       PASSWORD, USERNAME, JQL_BUG_STATUS,
                                                                       search_issue_by_name, search_all_issues,
                                                                       JQL_PROJECT_BUG_STATUS, JQL_PROJECT_BUG,
                                                                       Projects, record_info, JQL_BUGS, STRUCTURES,
                                                                       StatusesDeny)

bugs_schema = BugSchema(many=True)
bug_schema = BugSchema()


class AddBug(Resource):
    @record_info
    def post(self):
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
                description=issue.fields.summary
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


class UpdateBug(Resource):
    @record_info
    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        issue = search_issue_by_id(json_data['id'], USERNAME, PASSWORD)

        category = BugStructure.query.get(json_data['id'])

        if not category:
            return {'status': 'Category does not exist'}, 400

        if issue.fields.status.name in [i.value for i in StatusesDeny]:

            for f in set(STRUCTURES.keys()):

                category_t = STRUCTURES[f]['test_structure'].query.all()
                if category_t:
                    for test in set(category_t):
                        if test.bugs and int(json_data['id']) in test.bugs:
                            test.bugs = [i for i in test.bugs if i != int(json_data['id'])]
                            if not test.bugs:
                                test.skip = False

                category_s = STRUCTURES[f]['step_structure'].query.all()
                if category_s:
                    for step in set(category_s):
                        if step.bugs and int(json_data['id']) in step.bugs:

                            step.bugs = [i for i in step.bugs if i != int(json_data['id'])]
                            if not step.bugs:
                                step.skip = False

        category.name = issue.key
        category.status = issue.fields.status.name
        category.description = issue.fields.summary
        db.session.commit()

        data, errors = bug_schema.dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": 'success', 'data': data}, 200


class DeleteBug(Resource):
    @record_info
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        category = BugStructure.query.get(json_data['id'])
        if not category:
            return {'status': 'Category does not exist'}, 400

        for f in STRUCTURES.keys():

            category_t = STRUCTURES[f]['test_structure'].query.all()
            if category_t:
                for test in set(category_t):
                    if test.bugs and int(json_data['id']) in test.bugs:
                        test.bugs = [i for i in test.bugs if i != int(json_data['id'])]
                        if not test.bugs:
                            test.skip = False

            category_s = STRUCTURES[f]['step_structure'].query.all()
            if category_s:
                for step in set(category_s):
                    if step.bugs and json_data['id'] in step.bugs:

                        step.bugs = [i for i in step.bugs if i != json_data['id']]
                        if not step.bugs:
                            step.skip = False

        data, errors = bug_schema.dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        db.session.delete(category)
        db.session.commit()

        return {"status": 'success', 'data': data}, 200


class GetBug(Resource):
    @record_info
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        issue = search_issue_by_id(json_data['id'], USERNAME, PASSWORD)

        data = dict()

        data['name'] = issue.key
        data['url'] = issue.self
        data['summary'] = issue.fields.summary
        data['description'] = issue.fields.description
        data['statusName'] = issue.fields.status.name
        data['statusImg'] = issue.fields.status.iconUrl
        data['reporter'] = issue.fields.reporter.displayName
        data['priorityName'] = issue.fields.priority.name
        data['priorityImg'] = issue.fields.priority.iconUrl
        data['fixVersions'] = issue.fields.priority.iconUrl

        return {"status": 'success', 'data': data}, 200


class Bugs(Resource):

    @record_info
    def get(self):
        category = BugStructure.query.all()
        data, errors = bugs_schema.dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": "success", "data": data}, 200

    @record_info
    def post(self):
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
            category = BugStructure(
                id=issue.id,
                name=issue.key,
                status=issue.fields.status.name,
                description=issue.fields.summary
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
        category = BugStructure.query.all()

        for f in set(STRUCTURES.keys()):

            category_t = STRUCTURES[f]['test_structure'].query.all()
            if category_t:
                for test in set(category_t):
                    if test.bugs:
                        test.skip = False
                        test.bugs = []

            category_s = STRUCTURES[f]['step_structure'].query.all()
            if category_s:
                for step in set(category_s):
                    if step.bugs:
                        step.skip = False
                        step.bugs = []

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
                    for f in STRUCTURES.keys():

                        category_t = STRUCTURES[f]['test_structure'].query.all()
                        if category_t:
                            for test in set(category_t):
                                if test.bugs and int(issue.id) in test.bugs:
                                    test.bugs = [i for i in test.bugs if i != int(issue.id)]
                                    if not test.bugs:
                                        test.skip = False

                        category_s = STRUCTURES[f]['step_structure'].query.all()
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

        category = BugStructure.query.all()
        data, errors = bugs_schema.dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": 'success', 'data': data}, 200
