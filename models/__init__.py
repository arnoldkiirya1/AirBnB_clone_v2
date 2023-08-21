#!/usr/bin/python3
"""
This module initializes the storage variable.
"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
