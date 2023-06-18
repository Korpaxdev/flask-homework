from utils.sq import Sq
from utils.messages import Messages


def validate_required_fields(json_data, required_fields: list | tuple) -> list:
    errors = []
    for field in required_fields:
        if field not in json_data:
            errors.append({field: Messages.REQUIRED_FIELD})
    return errors


def validate_model_fields(json_data, model) -> list:
    errors = []
    required_errors = validate_required_fields(json_data, model.required_fields)
    if required_errors:
        return required_errors

    for field in model.required_fields:
        column = model.__table__.columns[field]
        data_value = json_data[field]
        column_length = getattr(column.type, "length", None)
        if column_length and len(str(data_value)) > column_length:
            errors.append({field: Messages.TOO_LONG_FIELD})
        if getattr(column, "unique", False):
            with Sq.get_session() as session:
                query = session.query(model).filter(column == data_value).first()
                if query:
                    errors.append({field: Messages.UNIQUE_FIELD})
    return errors


def validate_password_field(password) -> list:
    errors = []
    if len(str(password)) < 8:
        errors.append({"password": Messages.PASSWORD_TOO_SHORT})
    return errors


def clear_json_data(json_data: dict, required_fields: list | tuple):
    return {key: json_data[key] for key in json_data if key in required_fields}
