# -*- coding: utf-8 -*-
from marshmallow import fields, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

ma = Marshmallow()
db = SQLAlchemy()


# ************BUG STRUCTURES********************8
class BugStructure(db.Model):
    __tablename__ = 'bugs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, id, name, status, summary):
        self.id = id
        self.name = name
        self.status = status
        self.summary = summary


class BugSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    status = fields.String(required=True, validate=validate.Length(1))
    summary = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()



"""
**************************************************************************************
*                          STABLE-STRUCTURES                             *    WIN    *
**************************************************************************************
"""


# ******************CATEGORY STRUCTURES*******************
class WinCategoryStructure(db.Model):
    __tablename__ = 'win-category'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    components = db.relationship("WinComponentStructure", backref='components', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id


class WinCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    components = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************COMPONENT STRUCTURES*******************
class WinComponentStructure(db.Model):
    __tablename__ = 'win-component'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.String(150), ForeignKey('win-category.category_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    modules = db.relationship("WinModuleStructure", backref='modules', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id, component_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id
        self.component_id = component_id


class WinComponentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    modules = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************MODULE STRUCTURES*******************
class WinModuleStructure(db.Model):
    __tablename__ = 'win-module'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), ForeignKey('win-component.component_id', ondelete='CASCADE'))
    module_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    tests = db.relationship("WinTestStructure", backref='tests', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, component_id, skip, module_id):
        self.name = name
        self.component_id = component_id
        self.module_id = module_id
        self.skip = skip


class WinModuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    tests = fields.List(fields.Dict())
    skip = fields.Boolean(default=False)
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************TEST STRUCTURES********************
class WinTestStructure(db.Model):
    __tablename__ = 'win-test'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String(150), ForeignKey('win-module.module_id', ondelete='CASCADE'))
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    steps = db.relationship("WinStepStructure", backref='steps', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, module_id):
        self.test_id = test_id
        self.name = name
        self.skip = skip
        self.module_id = module_id


class WinTestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    steps = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************STEP STRUCTURES********************
class WinStepStructure(db.Model):
    __tablename__ = 'win-step'
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.String(150), nullable=False)
    test_id = db.Column(db.String(150), ForeignKey('win-test.test_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, description, step_id):
        self.name = name
        self.skip = skip
        self.test_id = test_id
        self.step_id = step_id
        self.description = description


class WinStepSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    step_id = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


"""
**************************************************************************************
*                         AN-MINOR-STRUCTURES                            *    WIN    *
**************************************************************************************
"""


# ******************CATEGORY STRUCTURES*******************
class WinMinorCategoryStructure(db.Model):
    __tablename__ = 'win-minor-category'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    components = db.relationship("WinMinorComponentStructure", backref='components', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id


class WinMinorCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    components = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************COMPONENT STRUCTURES*******************
class WinMinorComponentStructure(db.Model):
    __tablename__ = 'win-minor-component'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.String(150), ForeignKey('win-minor-category.category_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    modules = db.relationship("WinMinorModuleStructure", backref='modules', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id, component_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id
        self.component_id = component_id


class WinMinorComponentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    modules = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************MODULE STRUCTURES*******************
class WinMinorModuleStructure(db.Model):
    __tablename__ = 'win-minor-module'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), ForeignKey('win-minor-component.component_id', ondelete='CASCADE'))
    module_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    tests = db.relationship("WinMinorTestStructure", backref='tests', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, component_id, skip,module_id):
        self.name = name
        self.component_id = component_id
        self.module_id = module_id
        self.skip = skip


class WinMinorModuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    tests = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************TEST STRUCTURES********************
class WinMinorTestStructure(db.Model):
    __tablename__ = 'win-minor-tests'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String(150), ForeignKey('win-minor-module.module_id', ondelete='CASCADE'))
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    steps = db.relationship("WinMinorStepStructure", backref='steps', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, module_id):
        self.test_id = test_id
        self.name = name
        self.skip = skip
        self.module_id = module_id


class WinMinorTestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    steps = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************STEP STRUCTURES********************
class WinMinorStepStructure(db.Model):
    __tablename__ = 'win-minor-steps'
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.String(150), nullable=False)
    test_id = db.Column(db.String(150), ForeignKey('win-minor-tests.test_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, description, step_id):
        self.name = name
        self.skip = skip
        self.test_id = test_id
        self.step_id = step_id
        self.description = description


class WinMinorStepSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    step_id = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()



"""
**************************************************************************************
*                         AN-WEEKLY-STRUCTURES                           *    WIN    *
**************************************************************************************
"""


# ******************CATEGORY STRUCTURES*******************
class WinWeeklyCategoryStructure(db.Model):
    __tablename__ = 'win-an-weekly-category'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    components = db.relationship("WinWeeklyComponentStructure", backref='components', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id


class WinWeeklyCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    components = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    category_id = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()


# ******************COMPONENT STRUCTURES*******************
class WinWeeklyComponentStructure(db.Model):
    __tablename__ = 'win-an-weekly-component'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.String(150), ForeignKey('win-an-weekly-category.category_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    modules = db.relationship("WinWeeklyModuleStructure", backref='modules', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id, component_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id
        self.component_id = component_id


class WinWeeklyComponentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    modules = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************MODULE STRUCTURES*******************
class WinWeeklyModuleStructure(db.Model):
    __tablename__ = 'win-an-weekly-module'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), ForeignKey('win-an-weekly-component.component_id', ondelete='CASCADE'))
    module_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    tests = db.relationship("WinWeeklyTestStructure", backref='tests', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, component_id, skip, module_id):
        self.name = name
        self.component_id = component_id
        self.module_id = module_id
        self.skip = skip


class WinWeeklyModuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    tests = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************TEST STRUCTURES********************
class WinWeeklyTestStructure(db.Model):
    __tablename__ = 'win-an-weekly-tests'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String(150), ForeignKey('win-an-weekly-module.module_id', ondelete='CASCADE'))
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    steps = db.relationship("WinWeeklyStepStructure", backref='steps', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, module_id):
        self.test_id = test_id
        self.name = name
        self.skip = skip
        self.module_id = module_id


class WinWeeklyTestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    steps = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************STEP STRUCTURES********************
class WinWeeklyStepStructure(db.Model):
    __tablename__ = 'win-an-weekly-steps'
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.String(150), nullable=False)
    test_id = db.Column(db.String(150), ForeignKey('win-an-weekly-tests.test_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, description, step_id):
        self.name = name
        self.skip = skip
        self.test_id = test_id
        self.step_id = step_id
        self.description = description


class WinWeeklyStepSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    step_id = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()

"""
**************************************************************************************
*                          STABLE-STRUCTURES                             *    WIN    *
**************************************************************************************
"""


# ******************CATEGORY STRUCTURES*******************
class LinCategoryStructure(db.Model):
    __tablename__ = 'lin-category'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    components = db.relationship("LinComponentStructure", backref='components', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id


class LinCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    components = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************COMPONENT STRUCTURES*******************
class LinComponentStructure(db.Model):
    __tablename__ = 'lin-component'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.String(150), ForeignKey('lin-category.category_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    modules = db.relationship("LinModuleStructure", backref='modules', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id, component_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id
        self.component_id = component_id


class LinComponentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    modules = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************MODULE STRUCTURES*******************
class LinModuleStructure(db.Model):
    __tablename__ = 'lin-module'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), ForeignKey('lin-component.component_id', ondelete='CASCADE'))
    module_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    tests = db.relationship("LinTestStructure", backref='tests', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, component_id, skip, module_id):
        self.name = name
        self.component_id = component_id
        self.module_id = module_id
        self.skip = skip


class LinModuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    tests = fields.List(fields.Dict())
    skip = fields.Boolean(default=False)
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************TEST STRUCTURES********************
class LinTestStructure(db.Model):
    __tablename__ = 'lin-test'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String(150), ForeignKey('lin-module.module_id', ondelete='CASCADE'))
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    steps = db.relationship("LinStepStructure", backref='steps', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, module_id):
        self.test_id = test_id
        self.name = name
        self.skip = skip
        self.module_id = module_id


class LinTestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    steps = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************STEP STRUCTURES********************
class LinStepStructure(db.Model):
    __tablename__ = 'lin-step'
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.String(150), nullable=False)
    test_id = db.Column(db.String(150), ForeignKey('lin-test.test_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, description, step_id):
        self.name = name
        self.skip = skip
        self.test_id = test_id
        self.step_id = step_id
        self.description = description


class LinStepSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    step_id = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


"""
**************************************************************************************
*                         AN-MINOR-STRUCTURES                            *    WIN    *
**************************************************************************************
"""


# ******************CATEGORY STRUCTURES*******************
class LinMinorCategoryStructure(db.Model):
    __tablename__ = 'lin-minor-category'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    components = db.relationship("LinMinorComponentStructure", backref='components', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id


class LinMinorCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    components = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************COMPONENT STRUCTURES*******************
class LinMinorComponentStructure(db.Model):
    __tablename__ = 'lin-minor-component'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.String(150), ForeignKey('lin-minor-category.category_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    modules = db.relationship("LinMinorModuleStructure", backref='modules', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id, component_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id
        self.component_id = component_id


class LinMinorComponentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    modules = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************MODULE STRUCTURES*******************
class LinMinorModuleStructure(db.Model):
    __tablename__ = 'lin-minor-module'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), ForeignKey('lin-minor-component.component_id', ondelete='CASCADE'))
    module_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    tests = db.relationship("LinMinorTestStructure", backref='tests', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, component_id, skip,module_id):
        self.name = name
        self.component_id = component_id
        self.module_id = module_id
        self.skip = skip


class LinMinorModuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    tests = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************TEST STRUCTURES********************
class LinMinorTestStructure(db.Model):
    __tablename__ = 'lin-minor-tests'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String(150), ForeignKey('lin-minor-module.module_id', ondelete='CASCADE'))
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    steps = db.relationship("LinMinorStepStructure", backref='steps', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, module_id):
        self.test_id = test_id
        self.name = name
        self.skip = skip
        self.module_id = module_id


class LinMinorTestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    steps = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************STEP STRUCTURES********************
class LinMinorStepStructure(db.Model):
    __tablename__ = 'lin-minor-steps'
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.String(150), nullable=False)
    test_id = db.Column(db.String(150), ForeignKey('lin-minor-tests.test_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, description, step_id):
        self.name = name
        self.skip = skip
        self.test_id = test_id
        self.step_id = step_id
        self.description = description


class LinMinorStepSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    step_id = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()



"""
**************************************************************************************
*                         AN-WEEKLY-STRUCTURES                           *    WIN    *
**************************************************************************************
"""


# ******************CATEGORY STRUCTURES*******************
class LinWeeklyCategoryStructure(db.Model):
    __tablename__ = 'lin-an-weekly-category'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    components = db.relationship("LinWeeklyComponentStructure", backref='components', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id


class LinWeeklyCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    components = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    category_id = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()


# ******************COMPONENT STRUCTURES*******************
class LinWeeklyComponentStructure(db.Model):
    __tablename__ = 'lin-an-weekly-component'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.String(150), ForeignKey('lin-an-weekly-category.category_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    modules = db.relationship("LinWeeklyModuleStructure", backref='modules', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, category_id, component_id):
        self.name = name
        self.skip = skip
        self.category_id = category_id
        self.component_id = component_id


class LinWeeklyComponentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    category_id = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    modules = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ******************MODULE STRUCTURES*******************
class LinWeeklyModuleStructure(db.Model):
    __tablename__ = 'lin-an-weekly-module'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.String(150), ForeignKey('lin-an-weekly-component.component_id', ondelete='CASCADE'))
    module_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    tests = db.relationship("LinWeeklyTestStructure", backref='tests', passive_deletes=True)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, component_id, skip, module_id):
        self.name = name
        self.component_id = component_id
        self.module_id = module_id
        self.skip = skip


class LinWeeklyModuleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    component_id = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    tests = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************TEST STRUCTURES********************
class LinWeeklyTestStructure(db.Model):
    __tablename__ = 'lin-an-weekly-tests'
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String(150), ForeignKey('lin-an-weekly-module.module_id', ondelete='CASCADE'))
    test_id = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    steps = db.relationship("LinWeeklyStepStructure", backref='steps', passive_deletes=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, module_id):
        self.test_id = test_id
        self.name = name
        self.skip = skip
        self.module_id = module_id


class LinWeeklyTestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    module_id = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    steps = fields.List(fields.Dict())
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()


# ************STEP STRUCTURES********************
class LinWeeklyStepStructure(db.Model):
    __tablename__ = 'lin-an-weekly-steps'
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.String(150), nullable=False)
    test_id = db.Column(db.String(150), ForeignKey('lin-an-weekly-tests.test_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(550), nullable=False)
    skip = db.Column(db.Boolean, default=False, nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, skip, test_id, description, step_id):
        self.name = name
        self.skip = skip
        self.test_id = test_id
        self.step_id = step_id
        self.description = description


class LinWeeklyStepSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.String(required=True, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))
    step_id = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))
    skip = fields.Boolean(default=False)
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()