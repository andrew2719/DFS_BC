# import json
#
# json_data = {
#     "type": "upload",
#     "file_name": "test.txt"
# }
# converted_json = json.dumps(json_data) # converts to json(string)
#
# data = converted_json.encode() # converts to bytes
# print(data)
# data = data.decode() # converts to string
# print(data)
#
# converting_to_dict = json.loads(converted_json)
#
# print(converting_to_dict['type'])
#
# again_to_json = json.dumps(converting_to_dict)
#
# print(again_to_json)

import asyncio

tasks = []

async def task(i):
    print(i)
    await asyncio.sleep(2)
    print(i+1)
    return i

async def tasking():
    for i in range(10):
        tasks.append(asyncio.create_task(task(i)))

    x = await asyncio.gather(*tasks)
    print(x)

asyncio.run(tasking())