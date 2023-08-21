# client
import asyncio
import json

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    # print the status of the connection
    if writer.get_extra_info('peername') is not None:
        print(f'Connected to {writer.get_extra_info("peername")}')

        message = json.dumps(message)

        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(1024)
        print(f'Received: {data.decode()!r}')

        print('Close the connection')
        writer.close()
    else:
        print('Connection failed')

message = {
    "type": "self-upload",
    "file_name": "test.txt",
    "file": "hello world"
}

asyncio.run(tcp_echo_client(message))