from flask import Blueprint
from flask_restful import Api
from resources.Step import Step, Steps
from resources.Test import Test, Tests, TestUpdate
from resources.Bug import DeleteBug, Bugs, AddBug, UpdateBug, GetBug
from service_to_synchronize_tests_and_bugs.api.resources.Global import GlobalRequests
from service_to_synchronize_tests_and_bugs.api.resources.Module import Modules

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(Steps, '/steps')
api.add_resource(Step, '/step/<int:id>')

api.add_resource(Tests, '/tests')
api.add_resource(Test, '/test')
api.add_resource(TestUpdate, '/test/update')

api.add_resource(Bugs, '/bugs')
api.add_resource(DeleteBug, '/bug/delete')
api.add_resource(UpdateBug, '/bug/update')
api.add_resource(AddBug, '/bug/add')
api.add_resource(GetBug, '/bug')

# api.add_resource(TestRequest, '/test_request')

#
api.add_resource(Modules, '/modules')
# api.add_resource(ModuleRequest, '/module_request')


api.add_resource(GlobalRequests, '/global_requests')





