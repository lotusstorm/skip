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


class AddictionsStructure(db.Model):
    __tablename__ = 'addictions'
    id = db.Column(db.Integer, primary_key=True)
    current_id = db.Column(db.String(150), nullable=False)
    parent_id = db.Column(db.String(150), nullable=False)
    os = db.Column(db.String(150), nullable=False)
    branch = db.Column(db.String(150), nullable=False)
    issues = db.Column(db.PickleType, default=[], nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, current_id, parent_id, os, branch):
        self.current_id = current_id
        self.parent_id = parent_id
        self.os = os
        self.branch = branch


class AddictionsSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    current_id = fields.String(required=True, validate=validate.Length(1))
    parent_id = fields.String(required=True, validate=validate.Length(1))
    os = fields.String(required=True, validate=validate.Length(1))
    branch = fields.String(required=True, validate=validate.Length(1))
    issues = fields.List(fields.Int())
    creation_date = fields.DateTime()
