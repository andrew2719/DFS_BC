import json

# Read the json file
class Converter:
    def __init__(self,json_file):
        self.json_file = json_file

    #convert json file to dictionary
    async def json_to_dict(self):
        data = json.loads(self.json_file)
        return data

    #convert dictionary to json file and return it
    async def dict_to_json(self,dict):
        json_file = json.dumps(dict)
        return json_file