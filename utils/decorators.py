from flask import jsonify, request

from models.tokens import Tokens
from utils.json_message import json_message
from utils.messages import Messages
from utils.sq import Sq
from utils.tokens import get_token_from_headers
from utils.validation import (
    clear_json_data,
    validate_model_fields,
    validate_required_fields,
)


def full_validation_model(func):
    def wrapper(self, **kwargs):
        json_data = request.get_json()
        errors = validate_model_fields(json_data, self.model)
        if errors:
            return jsonify(errors), 400
        cleaned_json_data = clear_json_data(json_data, self.model.required_fields)
        kwargs.update(dict(json_data=cleaned_json_data))
        return func(self, **kwargs)

    return wrapper


def base_validation_by_required_fields(func):
    def wrapper(self, **kwargs):
        json_data = request.get_json()
        required_fields = self.model.required_fields
        errors = validate_required_fields(json_data, required_fields)
        if errors:
            return jsonify(errors), 400
        cleaned_json_data = clear_json_data(json_data, required_fields)
        kwargs.update(dict(json_data=cleaned_json_data))
        return func(self, **kwargs)

    return wrapper


def get_entry_from_model(func):
    def wrapper(self, **kwargs):
        with Sq.get_session() as session:
            object_id = kwargs.get("id")
            entry = session.query(self.model).get(object_id)
            if not entry:
                return json_message(Messages.NOT_FOUND, 404)
            kwargs.update(dict(entry=entry, session=session))
            return func(self, **kwargs)

    return wrapper


def get_entries_from_model(func):
    def wrapper(self, **kwargs):
        with Sq.get_session() as session:
            entries = session.query(self.model).all()
            kwargs.update(dict(entries=entries))
            return func(self, **kwargs)

    return wrapper


def auth_permission(func):
    def wrapper(self, **kwargs):
        with Sq.get_session() as session:
            token = get_token_from_headers(request.headers)
            if not token:
                return json_message(Messages.NOT_AUTHORIZED, 401)
            entry = session.query(Tokens).filter_by(token=token).first()
            if not entry:
                return json_message(Messages.NOT_AUTHORIZED, 401)
        kwargs.update(dict(user=entry, token=token))
        return func(self, **kwargs)

    return wrapper


def is_owner_advertisement_permission(func):
    @auth_permission
    def wrapper(self, **kwargs):
        user = kwargs.get("user")
        entry = kwargs.get("entry")
        if entry.owner != user.id:
            return json_message(Messages.NOT_OWNER_ADVERTISEMENT, 403)
        return func(self, **kwargs)

    return wrapper
