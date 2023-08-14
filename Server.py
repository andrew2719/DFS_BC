import asyncio

class Server:
    def __init__(self):
        self.port = 8888

    async def handle_echo(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")

        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()

        print("Close the connection")
        writer.close()

    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_echo, '0.0.0.0', self.port)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')
        async with server:
            await server.serve_forever()

    def run(self):
        asyncio.run(self.start_server())

if __name__ == "__main__":
    server = Server()
    server.run()