from flask import jsonify
from flask.views import MethodView

from models.tokens import Tokens
from models.users import Users
from serializers.tokens_serializer import TokenSerializer
from utils.decorators import base_validation_by_required_fields
from utils.sq import Sq
from utils.tokens import check_is_login, remove_token_by_user_id
from utils.users import get_user_by_json_data


class UserLogin(MethodView):
    model = Users

    @base_validation_by_required_fields
    def post(self, json_data):
        with Sq.get_session() as session:
            user, error = get_user_by_json_data(json_data)
            if error and not user:
                return jsonify(error)
            if check_is_login(user.id):
                remove_token_by_user_id(user.id)
            token = Tokens(user_id=user.id)
            session.add(token)
            session.commit()
            serializer = TokenSerializer(token)
            return jsonify(serializer.data)
