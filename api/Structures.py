from marshmallow import fields, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


# ************BUG STRUCTURES********************8
class BugStructure(db.Model):
    __tablename__ = 'bugs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, id, name, status, description):
        self.id = id
        self.name = name
        self.status = status
        self.description = description


class BugSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    status = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()



"""
**************************************************************************
*                          STABLE-STRUCTURES                             *
**************************************************************************
"""


# ************TEST STRUCTURES********************
class TestStructure(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    module_id = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    bugs = db.Column(db.PickleType, default=[], nullable=False)
    steps = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, module_id):
        self.test_id = test_id
        self.name = name
        self.skip = skip
        self.module_id = module_id


class TestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    steps = fields.List(fields.Dict())
    bugs = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************STEP STRUCTURES********************
class StepStructure(db.Model):
    __tablename__ = 'steps'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    step_id = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    bugs = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, description, step_id):
        self.name = name
        self.skip = skip
        self.test_id = test_id
        self.step_id = step_id
        self.description = description


class StepSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    step_id = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    bugs = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************MODULE STRUCTURES*******************
class ModuleStructure(db.Model):
    __tablename__ = 'module'
    id = db.Column(db.Integer, primary_key=True)
    categories = db.Column(db.String(150), nullable=False)
    components = db.Column(db.String(150), nullable=False)
    module_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, categories, components, module_id):
        self.name = name
        self.categories = categories
        self.components = components
        self.module_id = module_id


class ModuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    categories = fields.String(required=True, validate=validate.Length(1))
    components = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()


"""
**************************************************************************
*                         AN-MINOR-STRUCTURES                            *
**************************************************************************
"""


# ************TEST STRUCTURES********************
class MinorTestStructure(db.Model):
    __tablename__ = 'minor-tests'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    module_id = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    bugs = db.Column(db.PickleType, default=[], nullable=False)
    steps = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, module_id):
        self.test_id = test_id
        self.name = name
        self.skip = skip
        self.module_id = module_id


class MinorTestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    steps = fields.List(fields.Dict())
    bugs = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************STEP STRUCTURES********************
class MinorStepStructure(db.Model):
    __tablename__ = 'minor-steps'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    step_id = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    bugs = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, description, step_id):
        self.name = name
        self.skip = skip
        self.test_id = test_id
        self.step_id = step_id
        self.description = description


class MinorStepSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    step_id = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    bugs = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************MODULE STRUCTURES*******************
class MinorModuleStructure(db.Model):
    __tablename__ = 'minor-module'
    id = db.Column(db.Integer, primary_key=True)
    categories = db.Column(db.String(150), nullable=False)
    components = db.Column(db.String(150), nullable=False)
    module_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, categories, components, module_id):
        self.name = name
        self.categories = categories
        self.components = components
        self.module_id = module_id


class MinorModuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    categories = fields.String(required=True, validate=validate.Length(1))
    components = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()


"""
**************************************************************************
*                         AN-WEEKLY-STRUCTURES                           *
**************************************************************************
"""


# ************TEST STRUCTURES********************
class WeeklyTestStructure(db.Model):
    __tablename__ = 'an-weekly-tests'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    module_id = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    bugs = db.Column(db.PickleType, default=[], nullable=False)
    steps = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, module_id):
        self.test_id = test_id
        self.name = name
        self.skip = skip
        self.module_id = module_id


class WeeklyTestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    steps = fields.List(fields.Dict())
    bugs = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************STEP STRUCTURES********************
class WeeklyStepStructure(db.Model):
    __tablename__ = 'an-weekly-steps'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    step_id = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    bugs = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, description, step_id):
        self.name = name
        self.skip = skip
        self.test_id = test_id
        self.step_id = step_id
        self.description = description


class WeeklyStepSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    step_id = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    bugs = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************MODULE STRUCTURES*******************
class WeeklyModuleStructure(db.Model):
    __tablename__ = 'an-weekly-module'
    id = db.Column(db.Integer, primary_key=True)
    categories = db.Column(db.String(150), nullable=False)
    components = db.Column(db.String(150), nullable=False)
    module_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, categories, components, module_id):
        self.name = name
        self.categories = categories
        self.components = components
        self.module_id = module_id


class WeeklyModuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    categories = fields.String(required=True, validate=validate.Length(1))
    components = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()


if __name__ == '__main__':
    db.create_all()
