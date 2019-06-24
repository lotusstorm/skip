from flask import request
from flask_restful import Resource
from service_to_synchronize_tests_and_bugs.api.Structures import db
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import record_info, SCHEMAS, STRUCTURES


class Step(Resource):

    @record_info
    def get(self, id_):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[branch]['step_structure'].query.filter_by(test_id=id_).first()
        if not category:
            return {'status': 'Category does not exist'}, 400

        data, errors = SCHEMAS[branch]['steps_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        return {"status": "success", "data": data}, 200

    @record_info
    def delete(self, id_):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[branch]['step_structure'].query.get(id_)
        if not category:
            return {'status': 'Category does not exist'}, 400

        data, errors = SCHEMAS[branch]['step_schema'].dump(category)
        if errors:
            return {"status": "error", "data": errors}, 422

        db.session.delete(category)
        db.session.commit()

        return {"status": 'success', 'data': data}, 200


class Steps(Resource):

    @record_info
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch = json_data['branch']

        if branch not in STRUCTURES.keys() and branch not in SCHEMAS.keys():
            return {'status': 'Branch->{} is not supported'.format(branch)}, 400

        category = STRUCTURES[branch]['step_structure'].query.all()
        data, errors = SCHEMAS[branch]['steps_schema'].dump(category)
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
            category = STRUCTURES[branch]['step_structure'].query.filter_by(step_id=data['step_id']).first()
            if category:
                category.skip = data['skip']
                category.bugs = data['bugs']
                category.description = data['description']
        db.session.commit()

        category = STRUCTURES[branch]['step_structure'].query.all()
        data, errors = SCHEMAS[branch]['steps_schema'].dump(category)
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

        category = STRUCTURES[branch]['step_structure'].query.all()

        for el in category:
            db.session.delete(el)
        db.session.commit()

        category = STRUCTURES[branch]['step_structure'].query.all()
        data, errors = SCHEMAS[branch]['steps_schema'].dump(category)
        if data:
            return {"status": "db not cleaned"}, 422

        return {'status': 'db cleaned successfully', "data": data}, 200
