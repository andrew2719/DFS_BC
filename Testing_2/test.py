import asyncio

class Node:
    def __init__(self, port,peers = []):
        self.port = port
        self.peers = peers
        self.connections = set()


    async def handle_inbound(self, reader, writer):
        data = await reader.read(100)

        verification_result = await self.get_verification_from_system_b(data.decode())

        writer.write(verification_result.encode())
        await writer.drain()

    async def get_verification_from_system_b(self, data):
        reader, writer = await asyncio.open_connection('System_B_IP', 8888)
        writer.write(data.encode())
        await writer.drain()

        result = await reader.read(100)
        writer.close()
        await writer.wait_closed()

        return result.decode()

    async def start(self):
        server = await asyncio.start_server(self.handle_inbound, '0.0.0.0', self.port)
        async with server:
            await server.serve_forever()

async def main():
    node_a = Node(8888)
    await node_a.start()

asyncio.run(main())
