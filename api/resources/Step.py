# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from service_to_synchronize_tests_and_bugs.api.Structures import db
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import record_info, SCHEMAS, STRUCTURES, serializer


class Steps(Resource):

    @record_info
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']
        os = json_data['os']

        if os not in STRUCTURES.keys() or os not in SCHEMAS.keys():
            return {'status': 'OS->{} is not supported'.format(os)}, 400

        if branch not in STRUCTURES[os].keys() or branch not in SCHEMAS[os].keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[os][branch]['step_structure'].query.all()
        data, errors = SCHEMAS[os][branch]['steps_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": "success", "branch": branch, "data": serializer(os, branch, data)}, 200

    @record_info
    def put(self):
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
            category = STRUCTURES[os][branch]['step_structure'].query.filter_by(step_id=data['step_id']).first()
            if category:
                category.skip = data['skip']
                category.issues = data['issues']
                category.description = data['description']
        db.session.commit()

        category = STRUCTURES[os][branch]['step_structure'].query.all()
        data, errors = SCHEMAS[os][branch]['steps_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": 'success', "branch": branch, 'data': serializer(os, branch, data)}, 200

    @record_info
    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']
        os = json_data['os']

        if os not in STRUCTURES.keys() or os not in SCHEMAS.keys():
            return {'status': 'OS->{} is not supported'.format(os)}, 400

        if branch not in STRUCTURES[os].keys() or branch not in SCHEMAS[os].keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[os][branch]['step_structure'].query.all()

        for el in category:
            db.session.delete(el)
        db.session.commit()

        category = STRUCTURES[os][branch]['step_structure'].query.all()
        data, errors = SCHEMAS[os][branch]['steps_schema'].dump(category)
        if data:
            return {"status": "db not cleaned"}, 422

        return {'status': 'db cleaned successfully', "branch": branch, "data": serializer(os, branch, data)}, 200
