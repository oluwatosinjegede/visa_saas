from collections.abc import Mapping, Sequence

from rest_framework.views import exception_handler


def _to_error_dict(data):
    if data is None:
        return {}

    if isinstance(data, Mapping):
        result = {}
        for key, value in data.items():
            if isinstance(value, Mapping):
                result[key] = _to_error_dict(value)
            elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                result[key] = [str(item) for item in value]
            else:
                result[key] = [str(value)]
        return result

    if isinstance(data, Sequence) and not isinstance(data, (str, bytes)):
        return {"non_field_errors": [str(item) for item in data]}

    return {"non_field_errors": [str(data)]}


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    payload = response.data

    if isinstance(payload, Mapping) and "message" in payload and "errors" in payload:
        return response

    status_code = response.status_code
    default_message = "Request failed" if status_code >= 500 else "Validation failed"

    if isinstance(payload, Mapping) and "detail" in payload:
        message = str(payload.get("detail") or default_message)
        errors = _to_error_dict({"detail": payload.get("detail")})
    else:
        message = default_message
        errors = _to_error_dict(payload)

    response.data = {
        "message": message,
        "errors": errors,
    }
    return response
