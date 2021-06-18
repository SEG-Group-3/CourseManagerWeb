from enum import Flag, auto
from flask_login import UserMixin


class Permissions(Flag):
    # Admin
    DELETE_USERS = auto()
    CREATE_COURSES = auto()
    EDIT_COURSE = auto()

    # Instructor
    TEACH_COURSE = auto()
    EDIT_COURSE_INFO = auto()
    SEE_USERS = auto()

    # Student
    JOIN_COURSES = auto()


class Role:

    @staticmethod
    def from_user_type():
        return


class User(UserMixin):

    def __init__(self, data: dict) -> None:
        self.data = data
        super().__init__()

    @staticmethod
    def validate(parameters: dict) -> dict:
        return validate(parameters, ["userName", "realName", "password", "type"])

    def get_id(self):
        return self.data['userName']


class Course(UserMixin):

    @staticmethod
    def validate(parameters: dict) -> dict:
        return validate(parameters, ["code", "name"])


def validate(parameters: dict, required: list) -> dict:
    parameters = dict(parameters)
    sanitized = {}
    for key in required:
        if key in parameters.keys():
            sanitized[key] = parameters[key]
        else:
            sanitized[key] = None
    return sanitized
