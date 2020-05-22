from flask.json import JSONEncoder
from datetime import date, datetime
from uuid import UUID
from flask import current_app


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):  # pylint: disable=method-hidden
        try:
            if isinstance(obj, datetime) or isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)

            if isinstance(obj, UUID):
                return str(obj)

        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
