import uuid
from datetime import datetime, timedelta

from wtforms.validators import NumberRange

CACHE = {}

TOKEN_DURATION = 30


def _get_token_data(token):
    for v in CACHE.values():
        if v["token"] == token:
            return v
    return None


def get_token_data(token):
    tok = _get_token_data(token)
    if tok == None:
        return None

    now = datetime.now()
    expiration = tok.get("expiration")
    is_valid = now < expiration
    if not is_valid:
        delete_token(token)
        return None

    return tok


def delete_token(token) -> bool:
    CACHE.pop(token, None)


def delete_token_with_username(userName) -> bool:
    for k, _ in CACHE.items():
        if CACHE[k]["userName"] == userName:
            del CACHE[k]


def create_token(userName) -> dict:
    print("Creating tokens for " + userName)
    # Verify if token already exists delete it
    delete_token_with_username(userName)
    # Create new token
    tok = str(uuid.uuid4())
    expiration = datetime.now() + timedelta(minutes=TOKEN_DURATION)
    ret = {'token': tok, "userName": userName, "expiration": expiration}
    CACHE[tok] = ret
    return ret
