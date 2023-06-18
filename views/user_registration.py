from flask import jsonify
from flask.views import MethodView

from models.users import Users
from serializers.user_serializer import UserSerializer
from utils.decorators import full_validation_model
from utils.sq import Sq
from utils.validation import validate_password_field


class UserRegistrationView(MethodView):
    model = Users

    @full_validation_model
    def post(self, json_data, **kwargs):
        with Sq.get_session() as session:
            errors = validate_password_field(json_data["password"])
            if errors:
                return jsonify(errors), 400
            user = self.model(**json_data)
            session.add(user)
            session.commit()
            serializer = UserSerializer(user)
        return jsonify(serializer.data), 201
