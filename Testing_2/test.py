import asyncio
from concurrent.futures import ThreadPoolExecutor


class Node:
    def __init__(self, port, peers=[]):
        self.port = port
        self.peers = peers
        self.connections = []

    async def handle_inbound(self, reader, writer):
        print("handle_inbound opened")
        addr = writer.get_extra_info('peername')
        print(f"Connected to {addr}")
        while True:
            print("waiting for data in handle_inbound")
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()
            print(f"Received in inbound: {message} from {addr}")

            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as pool:
                response = await loop.run_in_executor(pool, input, "Reply message in inbound: ")

            response = f"response from inbound {self.port}: {response}"
            writer.write(response.encode())
            print(f"Sent: {response} to {addr}")
            await writer.drain()

    async def initiate_outbound(self, ip, port=8888):
        print("initiate_outbound opened")
        reader, writer = await asyncio.open_connection(ip, port)
        print("outbound connected to", ip, ":", port)

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            while True:
                message = await loop.run_in_executor(pool, input, "Enter message in outbound: ")
                message = f'{self.port}: {message}'
                writer.write(message.encode())
                print(f"Sent from outbound: {message} to {ip}:{port}")
                await writer.drain()
                data = await reader.read(100)
                print(f"Received in outbound: {data.decode()} from {ip}:{port}")

    async def start(self):
        # This will start our server to listen for inbound connections
        server = await asyncio.start_server(self.handle_inbound, '0.0.0.0', self.port)
        addr = server.sockets[0].getsockname()
        print(f'Started Node on {addr}')

        # Establish outbound connections
        for peer_ip in self.peers:
            asyncio.create_task(self.initiate_outbound(peer_ip))

        # The server will run indefinitely, listening for connections
        await server.serve_forever()


async def main():
    node = Node(8888, ['172.21.10.37'])
    await node.start()


asyncio.run(main())
