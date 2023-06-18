from flask import jsonify, request
from flask.views import MethodView

from models.advertisements import Advertisements
from serializers.advertisiments_serializers import AdvertisementDetailSerializer
from utils.decorators import (
    full_validation_model,
    get_entry_from_model,
    is_owner_advertisement_permission,
)
from utils.json_message import json_message
from utils.messages import Messages


class AdvertisementDetailView(MethodView):
    model = Advertisements

    @get_entry_from_model
    def get(self, entry, **kwargs):
        serializer = AdvertisementDetailSerializer(entry)
        return jsonify(serializer.data)

    @get_entry_from_model
    @is_owner_advertisement_permission
    def delete(self, entry, session, **kwargs):
        session.delete(entry)
        session.commit()
        return json_message(Messages.MESSAGE_DELETED)

    @get_entry_from_model
    @is_owner_advertisement_permission
    @full_validation_model
    def put(self, json_data, entry, session, **kwargs):
        keys = self.model.required_fields
        for key in keys:
            if key in json_data:
                setattr(entry, key, json_data[key])
        session.commit()
        serializer = AdvertisementDetailSerializer(entry)
        return jsonify(serializer.data)

    @get_entry_from_model
    @is_owner_advertisement_permission
    def patch(self, entry, session, **kwargs):
        json_data = request.get_json()
        available_keys = self.model.required_fields
        for key in available_keys:
            if key in json_data:
                setattr(entry, key, json_data[key])
        session.commit()
        serializer = AdvertisementDetailSerializer(entry)
        return jsonify(serializer.data)
