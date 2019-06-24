# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import record_info, STRUCTURES, SCHEMAS
from service_to_synchronize_tests_and_bugs.api.Structures import db


class Modules(Resource):

    @record_info
    def post(self):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[branch]['module_structure'].query.all()
        data, errors = SCHEMAS[branch]['modules_schema'].dump(category)
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
            category = STRUCTURES[branch]['module_structure'].query.filter_by(module_id=data['module_id']).first()
            if category:
                category.categories = data['categories']
                category.components = data['components']
        db.session.commit()

        category = STRUCTURES[branch]['module_structure'].query.all()
        data, errors = SCHEMAS[branch]['modules_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": 'success', 'data': data}, 200
