# -*- coding: utf-8 -*-
from flask import request, send_file
from flask_restful import Resource

from ecosystem_settings import EcosystemSettings
from excel_manager import ExcelManager
from mercurial_lib.hg_updater import HGClientWrapper
from service_to_synchronize_tests_and_bugs.api.helpers_for_api import (record_info, get_from_db, update_in_db,
                                                                       issue_binder, get_name_from_id, issue_repr,
                                                                       tree_, OUT_PATH, start_in_another_process, PATH)
from service_to_synchronize_tests_and_bugs.api.Structures import db, AddictionsStructure
from service_to_synchronize_tests_and_bugs.api.tests_creater import tests_creater


class GlobalUpdate(Resource):

    @record_info
    def put(self):
        """
        Запрос для обновления состояния тестов в БД
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status': 'No input data provided'}, 400

        branch_ = json_data['branch']
        os_ = json_data['os']
        json_data = json_data['data']

        arr = tree_(data=json_data, target=update_in_db, kwargs={'os': os_, 'branch': branch_})
        db.session.commit()

        return {"status": 'success', 'data': arr}, 200


class GenerateReport(Resource):

    @record_info
    def post(self):
        """
        Запрос для скачивания отчета в формате .xls
        """
        exl = ExcelManager()

        conf = set([(h.os, h.branch) for h in AddictionsStructure.query.all()])
        for h in conf:
            items = AddictionsStructure.query.filter_by(os=h[0], branch=h[1]).all()
            exl.add_sheet('{}_{}'.format(*h))
            a = set([i.parent_id for i in items])
            for f in a:
                g = AddictionsStructure.query.filter_by(os=h[0], branch=h[1], parent_id=f).all()

                issues = ('\n').join([i['name'] for i in issue_repr(issue_binder([i.issues for i in g]))])
                for j in g:
                    s = ('\n').join([i['name'] for i in issue_repr(j.issues)])
                    exl.write(get_name_from_id(j.parent_id), issues, get_name_from_id(j.current_id), s)

        exl.save(OUT_PATH.format("report"))

        return send_file(OUT_PATH.format("report"), as_attachment=True, mimetype='text/xls')


class GlobalGetter(Resource):

    @record_info
    def post(self):
        """
        Запрос для получения иерархии тестов в формате json
        """
        req = request.get_json(force=True)

        if not req:
            return {'status': 'No input data provided'}, 400

        branch_ = req['branch']
        os_ = req['os']

        HGClientWrapper.pull_and_update_to_head(hg_dir=EcosystemSettings.ROOT_DIR,
                                                source="https://vonegosh:Zamolchisvoirot1@bitbucket.org/Axxonsoft/axxonnext_autotests",
                                                branch=branch_) #IMPORTANT раскоментить

        json_data = start_in_another_process(tests_creater, PATH)
        arr = tree_(data=json_data, target=get_from_db, kwargs={'os': os_, 'branch': branch_})
        db.session.commit()

        return {"status": 'success', 'data': arr}, 200
