import asyncio
import os

class FileServer:
    def __init__(self, port, save_path='./received_files'):
        self.port = port
        self.files = {}  # {IP: file_path}
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)

    async def handle_inbound(self, reader, writer):
        # Get sender's IP
        addr = writer.get_extra_info('peername')[0]

        # First, read the file size
        size_header = await reader.read(10)  # Let's say 10 bytes for the file size header
        file_size = int(size_header.decode().strip())

        # Now, read the actual file content
        file_content = await reader.readexactly(file_size)

        # Save to a file
        file_path = os.path.join(self.save_path, f"{addr.replace('.', '_')}.file")
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Save the path in the dictionary
        self.files[addr] = file_path

        # Send acknowledgment
        writer.write(b"File received and saved successfully!")
        await writer.drain()

    async def start(self):
        server = await asyncio.start_server(self.handle_inbound, '0.0.0.0', self.port)
        async with server:
            await server.serve_forever()

    def open_file(self, ip):
        file_path = self.files.get(ip)
        if file_path and os.path.exists(file_path):
            # This will use the default program associated with the file type to open it.
            os.system(f"open {file_path}")  # This is for macOS, adjust for other OSes

async def main():
    server = FileServer(8888)
    await server.start()

# Start the server
asyncio.run(main())
