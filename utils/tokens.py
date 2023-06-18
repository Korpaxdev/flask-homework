import re
import uuid

from utils.sq import Sq
from models.tokens import Tokens


def get_token_from_headers(headers):
    authorization = headers.get('Authorization')
    if not authorization:
        return None
    token = re.match(r'Token\s+(.+)', authorization)
    if token and token.group(1):
        return get_uuid_from_string(token.group(1))
    return None


def get_uuid_from_string(string: str):
    try:
        return uuid.UUID(string)
    except ValueError:
        return None


def check_is_login(user_id: int):
    with Sq.get_session() as session:
        token = session.query(Tokens).filter_by(user_id=user_id).first()
        return bool(token)


def remove_token(token):
    with Sq.get_session() as session:
        entry = session.query(Tokens).filter_by(token=token).first()
        if not entry:
            return False
        session.delete(entry)
        session.commit()
        return True


def remove_token_by_user_id(user_id):
    with Sq.get_session() as session:
        entry = session.query(Tokens).filter_by(user_id=user_id).first()
        if not entry:
            return False
        session.delete(entry)
        session.commit()
        return True


def check_authorization(token):
    with Sq.get_session() as session:
        return bool(session.query(Tokens).filter_by(token=token).first())
