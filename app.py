from flask import Flask
from flask_cors import CORS, cross_origin
from flask.json import JSONEncoder
from datetime import datetime

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
app = Flask(__name__)
CORS(app)
app.json_encoder = CustomJSONEncoder