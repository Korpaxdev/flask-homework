from flask import jsonify
from flask.views import MethodView

from models.advertisements import Advertisements
from serializers.advertisiments_serializers import (
    AdvertisementDetailSerializer,
    AdvertisementsSerializer,
)
from utils.decorators import (
    auth_permission,
    full_validation_model,
    get_entries_from_model,
)
from utils.sq import Sq


class IndexView(MethodView):
    model = Advertisements

    @get_entries_from_model
    def get(self, entries, **kwargs):
        serializer = AdvertisementsSerializer(entries)
        return jsonify(serializer.data)

    @auth_permission
    @full_validation_model
    def post(self, json_data, user, **kwargs):
        with Sq.get_session() as session:
            json_data["owner"] = user.id
            advertisement = self.model(**json_data)
            session.add(advertisement)
            session.commit()
            serializer = AdvertisementDetailSerializer(advertisement)
        return jsonify(serializer.data), 201
