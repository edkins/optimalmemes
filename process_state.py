import json
import jsonschema

class JsonSchema:
    def __init__(self, filename):
        self.schema = json.load(open(filename))

    def parse_filename(self, filename):
        obj = json.load(open(filename))
        jsonschema.validate(obj, self.schema)
        return obj

state_schema = JsonSchema('state-schema.json')

print(state_schema.parse_filename('state.json'))

