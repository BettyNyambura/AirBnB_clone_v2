#!/usr/bin/python3
"""This module instantiates an instance of the Storage will be used"""

from os import getenv

storage_time = getenv('HBNB_TYPE_STORAGE', 'file')

if storage_time == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
