from typing import Type, Tuple

from utils.sq import Sq
from models.users import Users
from utils.messages import Messages
from utils.password_hash import check_password

GetUserType = Tuple[Type[Users] | None, dict | None]


def get_user_by_json_data(json_data: dict) -> GetUserType:
    with Sq.get_session() as session:
        email = json_data['email']
        user = session.query(Users).filter_by(email=email).first()
        if not user:
            return user, {"message": Messages.USER_NOT_FOUND}
        password = json_data['password']
        if not check_password(password, user.password):
            user = None
            return user, {'message': Messages.WRONG_EMAIL_OR_PASS}
        return user, None
