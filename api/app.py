from flask import Blueprint
from flask_restful import Api
from resources.Test import TestUpdate
from resources.Issue import DeleteIssue, Issues, AddIssue, UpdateIssue, GetIssue
from resources.Global import GlobalUpdate, GenerateReport, GlobalGetter

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(TestUpdate, '/test/update')

api.add_resource(Issues, '/issues')
api.add_resource(DeleteIssue, '/issue/delete')
api.add_resource(UpdateIssue, '/issue/update')
api.add_resource(AddIssue, '/issue/add')
api.add_resource(GetIssue, '/issue')

api.add_resource(GlobalUpdate, '/global_update')

api.add_resource(GenerateReport, '/generate_report')
api.add_resource(GlobalGetter, '/data')






