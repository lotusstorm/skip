from flask import Blueprint
from flask_restful import Api
from resources.Step import Steps
from resources.Test import Tests, TestUpdate
from resources.Issue import DeleteIssue, Issues, AddIssue, UpdateIssue, GetIssue
from resources.Global import GlobalRequests, GlobalUpdate
from resources.Module import Modules
from resources.Category import Category
from resources.Component import Component

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(Steps, '/steps')

api.add_resource(Tests, '/tests')
api.add_resource(TestUpdate, '/test/update')

api.add_resource(Issues, '/issues')
api.add_resource(DeleteIssue, '/issue/delete')
api.add_resource(UpdateIssue, '/issue/update')
api.add_resource(AddIssue, '/issue/add')
api.add_resource(GetIssue, '/issue')

api.add_resource(Category, '/categories')
api.add_resource(Component, '/components')
api.add_resource(Modules, '/modules')

api.add_resource(GlobalRequests, '/global_requests')
api.add_resource(GlobalUpdate, '/global_update')





