import json
import logging
from collections.abc import Mapping

from rest_framework.utils.encoders import JSONEncoder


class CustomLoggingEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except Exception:
            if hasattr(obj, "__str__"):
                return str(obj)
            elif hasattr(obj, "__class__"):
                return str(obj.__class__)
            return "N/A"


class CustomStreamHandler(logging.StreamHandler):
    """
    Overrides StreamHandler, adding conditional to check if the
    message being logged is of abstract type Mapping, like dict,
    collections.defaultdict, collections.OrderedDict and collections.Counter.
    If it is then serialize obj to json str so logging systems that supports
    json can use, e.g. Amazon CloudWatch
    """

    def emit(self, record: logging.LogRecord) -> None:
        if isinstance(record.msg, Mapping):
            record.msg = json.dumps(record.msg, cls=CustomLoggingEncoder)
        super().emit(record)
