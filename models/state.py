#!/usr/bin/python3
# module that defines State class
from models.base_model import BaseModel


class State(BaseModel):
    def __init__(self, name="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
