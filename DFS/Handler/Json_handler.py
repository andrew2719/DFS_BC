import json

# take the json and convert to dict
async def to_dict(json_data):
    return json.loads(json_data.decode('utf-8'))

# take the dict and convert to json
async def to_json(dict_data):
    return json.dumps(dict_data).encode('utf-8')
