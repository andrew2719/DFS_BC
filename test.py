import json

json_data = {
    "type": "upload",
    "file_name": "test.txt"
}
converted_json = json.dumps(json_data) # converts to json

data = converted_json.encode() # converts to bytes
print(data)
data = data.decode() # converts to string
print(data)

converting_to_dict = json.loads(converted_json)

print(converting_to_dict['type'])

again_to_json = json.dumps(converting_to_dict)

print(again_to_json)