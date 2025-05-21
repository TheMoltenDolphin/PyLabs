import json
import jsonschema

with open("ex_1.json") as file:
    data = json.load(file)

with open("1_json_schema.json") as file:
    schema = json.load(file)


try:
    jsonschema.validate(instance=data, schema=schema)
    print("Validation passed")
except jsonschema.exceptions.ValidationError as e:
    print(f"Error of validation: {e.message}")