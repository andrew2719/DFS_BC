import asyncio
import socket
from Handler import HandleSelf, HandleIncoming
from Messages import *

# get the ip of the system
SYSTEM_IP = socket.gethostbyname(socket.gethostname())

class Server:
    def __init__(self):
        self.port = 8888

    async def handle_echo(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Received connection from {addr}")
        data = await reader.read(4096)
        dict_data = await Converter(data.decode()).json_to_dict()
        print(dict_data)

        # self-X represents the client function of the same system
        if dict_data['type'] == 'self-upload':

            #creating a handler object that can send the data to the handler
            #the handler will handle the request and return the response
            #the response is the list of the responses from the peers

            handler = HandleSelf(dict_data,reader,writer)
            response = await handler.handle()
            print(response,"from server")

            writer.write("responses generated".encode())
            await writer.drain()

        elif dict_data['type'] == 'server-upload':
            # data = await reader.read(4096)
            print(data.decode())
            writer.write("back reply".encode())
            await writer.drain()


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