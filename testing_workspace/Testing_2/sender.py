import asyncio
import os
import aiofiles
import json
from tkinter import filedialog
from tkinter import Tk
import hashlib

async def get_extension(file_path):
    return os.path.splitext(file_path)[1]
async def generate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(1024):
            hasher.update(chunk)
    return hasher.hexdigest()
async def send_file(file_path, server_ip, server_port):
    reader, writer = await asyncio.open_connection(server_ip, server_port)

    # Send the file name length and file name
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    file_name_size = len(file_name)
    file_info = {"REQUEST": "UPLOAD",
                            "NODE":"NODE",
                            "file_name": file_name,
                            "file_size": file_size}
    # get a hash for fileinfo
    dumped = json.dumps(file_info)
    file_info_hash = hashlib.sha256(dumped.encode('utf-8')).hexdigest()
    extension = await get_extension(file_path)
    file_info['file_name'] = file_info_hash

    file_info = json.dumps(file_info)
    writer.write(file_info.encode('utf-8')) # Send file info at first
    await writer.drain()
    hash_of_the_file = await generate_file_hash(file_path)
    print(hash_of_the_file)

    # Send the file
    print("Uploading...")

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            writer.write(chunk)
            await writer.drain()

    # Get JSON acknowledgment
    ack_data = await reader.read(1024)
    ack_json = json.loads(ack_data.decode('utf-8'))
    print(f"Received: {ack_json}")

    if ack_json['hash'] == hash_of_the_file:
        print("File sent successfully.")

    else:
        print("File sent successfully but hash mismatched.")

    writer.close()
    await writer.wait_closed()

# GUI for file selection
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

if file_path:
    asyncio.run(send_file(file_path, '127.0.0.1', 8888))
else:
    print("No file selected.")

