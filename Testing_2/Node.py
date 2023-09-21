import asyncio
import aiofiles
import os
import json
from collections import defaultdict

class Node:
    def __init__(self, port, peers=[], save_path='./received_files'):
        self.port = port
        self.peers = peers
        self.peer_connections = {}  # To store connection objects for peers
        self.files = {}  # {IP: file_path}
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)


    async def connections(self):
        return self.peer_connections
    async def handle_inbound(self, reader, writer):
        addr = writer.get_extra_info('peername')[0]
        print(f"Node {self.port} received connection from {addr}")

        file_info = await reader.read(1024)
        file_info = json.loads(file_info.decode('utf-8'))

        print(file_info)

        file_name = file_info['file_name']
        file_size = file_info['file_size']

        # Create a 'received_files' directory if it doesn't exist
        if not os.path.exists('received_files'):
            os.mkdir('received_files')

        # Write the incoming file data to a new file
        size = 0
        async with aiofiles.open(f'received_files/{file_name}', 'wb') as f:
            while size < file_size:
                chunk = await reader.read(1024)
                print(f"chunk: {chunk} , len: {len(chunk)}")
                size += len(chunk)

                if size > file_size:
                    print("Received more data than expected, breaking.")
                    break

                if size == file_size or chunk == b'':
                    print("End of file, breaking.")
                    await f.write(chunk)
                    break
                else:
                    await f.write(chunk)

        # Send a JSON acknowledgment
        ack_data = {"status": "success", "detail": "File received successfully"}
        writer.write(json.dumps(ack_data).encode('utf-8'))
        await writer.drain()
        writer.close()

    async def send_data_to_peers(self, data):
        # This will send data to all connected peers
        verification_result = []
        for peer_ip in self.peer_connections:
            reader, writer = self.peer_connections[peer_ip]
    #         send them to verification
            writer.write(data.encode())
            await writer.drain()
            result = [peer_ip,await self.verification(reader,writer)]
            verification_result.append(result)

        print(verification_result)
        return verification_result

    async def verification(self,reader,writer):
        data = await reader.read(100)
        print(f"Node {self.port} received: {data.decode()}")
        writer.write("verification done".encode())
        await writer.drain()

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
    node = Node(8888, ['172.21.10.37', '172.21.10.38'])
    await node.start()

if __name__ == '__main__':
    asyncio.run(main())
