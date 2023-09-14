import asyncio

class Node:
    def __init__(self, port, peers=[]):
        self.port = port
        self.peers = peers
        self.connections = []

    async def handle_inbound(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connected to {addr}")
        while True:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()
            print(f"Received: {message} from {addr}")
            response = f"Echo from {self.port}: {message}"
            writer.write(response.encode())
            await writer.drain()

    async def initiate_outbound(self, ip, port=8888):
        reader, writer = await asyncio.open_connection(ip, port)
        while True:
            message = f"Hello from {self.port}"
            writer.write(message.encode())
            await writer.drain()
            data = await reader.read(100)
            print(f"Received: {data.decode()} from {ip}:{port}")

    async def start(self):
        # This will start our server to listen for inbound connections
        server = await asyncio.start_server(self.handle_inbound, '0.0.0.0', self.port)
        addr = server.sockets[0].getsockname()
        print(f'Started Node on {addr}')

        # Establish outbound connections
        for peer_ip in self.peers:
            asyncio.create_task(self.initiate_outbound(peer_ip)) # tries to make connection to the peers( the knows ip addresses)

        # The server will run indefinitely, listening for connections
        await server.serve_forever()

async def main():
    node = Node(8888, ['10.10.5.148'])
    await node.start()

asyncio.run(main())
