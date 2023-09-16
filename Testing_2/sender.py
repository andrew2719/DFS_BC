import asyncio

async def send_data_to_local_server(data):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(f"LOCAL_SEND:{data}".encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

# CLI example:
if __name__ == "__main__":
    data = input("Enter the data to send: ")
    asyncio.run(send_data_to_local_server(data))
