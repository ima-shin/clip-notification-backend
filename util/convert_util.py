import json
from datetime import date, datetime


def convert_model_to_json(model):
    """引数のモデルをJSON形式に変換"""
    if not model:
        return {}
    res = {}
    for key, value in model.__dict__.values():
        print(value)
        if isinstance(value, (datetime, date)):
            value = value.isoformat()
            print(value)
        res[key] = value
    return json.dumps(res)
