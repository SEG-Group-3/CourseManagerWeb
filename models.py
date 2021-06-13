class User:
    @classmethod
    def validate(cls, parameters: dict) -> dict:
        return validate(parameters, ["userName", "realName", "password", "type"])


class Course:
    @classmethod
    def validate(cls, parameters: dict) -> dict:
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
