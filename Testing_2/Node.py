import asyncio
import aiofiles
import os
import json
import Handler
import hashlib

class Node:
    def __init__(self, port, peers=[], save_path='./received_files'):
        self.port = port
        self.peers = peers
        self.peer_connections = {}  # To store connection objects for peers
        self.files = {}  # {IP: file_path}
        self.save_path = save_path

        if not os.path.exists(save_path):
            os.makedirs(save_path)

    async def save_file_object_to_disk(self,file_obj, save_path,ip):
        async with aiofiles.open(f"{save_path}/{ip}_{file_obj.file_name}", 'wb') as f:
            await f.write(file_obj.data)

    async def handle_UPLOAD(self, reader, writer, file_info):

        handler = Handler.Handle(file_info,reader,writer)
        file_obj = await handler.HandleUpload()

        return file_obj # this contains the data and the hash of the file

    async def handle_inbound(self, reader, writer):
        # writer.get_extra_info('peername') returns like this "('127.0.0.1', 30470)"
        addr = writer.get_extra_info('peername')[0]
        print(f"Node {self.port} received connection from {addr}")

        file_info_data = await reader.read(1024)
        file_info = json.loads(file_info_data.decode('utf-8'))


        if file_info["REQUEST"] == "UPLOAD":
            file_obj = await self.handle_UPLOAD(reader, writer, file_info)

            if file_info["NODE"] == "SELF":
                # we need to send them to the peers
                # with some procedures
                pass

            else:
                print(file_obj.hasher.hexdigest())
                ack_data = {
                                "status": "success",
                                "detail": "File received successfully",
                                "hash": file_obj.hasher.hexdigest()
                            }
                writer.write(json.dumps(ack_data).encode('utf-8'))
                await writer.drain()
                writer.close()

                await self.save_file_object_to_disk(file_obj, self.save_path,addr)

    async def send_to_peer(self, peer_ip, file_obj):
        reader, writer = self.peer_connections[peer_ip]
        file_info = json.dumps({"REQUEST": "UPLOAD",
                                "NODE":"NODE",
                                "file_name": file_obj.file_name,
                                "file_size": file_obj.file_size})
        writer.write(file_info.encode('utf-8')) # Send file info at first

        await writer.drain()

    async def send_to_all_peers(self, file_obj):
        tasks = []
        for peer_ip in self.peer_connections.keys():
            task = asyncio.create_task(self.send_to_peer(peer_ip, file_obj))
            tasks.append(task)

        await asyncio.gather(*tasks)


    async def connect_to_peer(self, peer_ip, port=8888):
        try:
            reader, writer = await asyncio.open_connection(peer_ip, port)
            self.peer_connections[peer_ip] = (reader, writer)
            print(f"Node {self.port} connected to peer {peer_ip}:{port}")
        except Exception as e:
            print(f"Error connecting to {peer_ip}:{port}. Error: {e}")

    async def start(self):
        # Starting server to listen for inbound connections
        server = await asyncio.start_server(self.handle_inbound, '0.0.0.0', self.port)
        print(f'Started Node on {self.port}')

        # Connect to all known peers
        for peer in self.peers:
            asyncio.create_task(self.connect_to_peer(peer))

        await server.serve_forever()

async def main():
    # Node initialized with peers (replace with your IPs)
    node = Node(8888, ['10.10.2.113'])
    await node.start()

if __name__ == '__main__':
    asyncio.run(main())
