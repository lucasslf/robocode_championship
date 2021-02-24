# -*- coding: utf-8 -*-

import decimal

import uuid
import json
from json import JSONEncoder

from dataclasses import is_dataclass, asdict


def dumps(data, sort_keys=False, **options):

    encoder = ExtendedEncoder
    return json.dumps(
        data,
        cls=encoder,
        sort_keys=sort_keys,
        separators=(',', ':'),
        **options,
    )


def loads(json_data):

    return json.loads(json_data)


class ExtendedEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        if hasattr(obj, 'serialize'):
            return obj.serialize()
        if is_dataclass(obj):
            return asdict(obj)
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        else:
            return super().default(obj)
