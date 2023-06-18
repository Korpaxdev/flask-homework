from flask import request
from flask.views import MethodView

from utils.json_message import json_message
from utils.messages import Messages
from utils.tokens import get_token_from_headers, remove_token


class UserLogoutView(MethodView):
    @staticmethod
    def post():
        token = get_token_from_headers(request.headers)
        if not token:
            return json_message(Messages.NOT_AUTHORIZED, 401)
        if remove_token(token):
            return json_message(Messages.LOGOUT_SUCCESS)
        return json_message(Messages.TOKEN_NOT_FOUND, 400)
