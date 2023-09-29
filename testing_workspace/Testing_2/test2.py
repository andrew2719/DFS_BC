import asyncio

class Node:
    def __init__(self, port, peers=[]):
        self.port = port
        self.peers = peers
        self.peer_connections = {}  # To store connection objects for peers

    async def handle_inbound(self, reader, writer):
        # This will handle data received from other nodes
        data = await reader.read(100)
        print(f"Node {self.port} received: {data.decode()}")

        # You can further process data here and use self.peer_connections to send data to peers
        verified_result = await self.send_data_to_peers(data.decode())
        print("verified_result : ",verified_result)

        if verified_result:
            writer.write("verified".encode())
            await writer.drain()

        else:
            writer.write("not verified".encode())
            await writer.drain()


    async def send_data_to_peers(self, data):
        # This will send data to all connected peers
        verification_result = []
        for peer_ip in self.peer_connections:
            reader, writer = self.peer_connections[peer_ip]
    #         send them to verification
            writer.write(data.encode())
            await writer.drain()

            verification_result.append(await self.verification(reader,writer))

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

asyncio.run(main())
