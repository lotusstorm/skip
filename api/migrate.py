# -*- coding: utf-8 -*-
import os
import logging

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from Structures import db
from runner import create_app

DIR_NAME = 'db'
logger = logging.getLogger('axxon')
app = create_app('config')
migrate = Migrate(app, db)
manager = Manager(app)

if not os.path.exists(DIR_NAME):
    try:
        os.makedirs(DIR_NAME)
    except Exception:
        msg = 'Unable to create extract folder'
        logger.error(msg)
        raise Exception(msg)

manager.add_command(DIR_NAME, MigrateCommand)


if __name__ == '__main__':
    manager.run()
    # python migrate.py db init
    # python migrate.py db migrate -m ""
    # python migrate.py db upgrade

