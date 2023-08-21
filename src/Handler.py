import asyncio
PEERS = ['192.168.159.77']

class HandleSelf:
    def __init__(self,data,reader,writer):
        self.data = data
        self.reader = reader
        self.writer = writer
    async def handle(self):
        if self.data['type'] == 'upload':
            return await self.handle_upload()
        elif self.data['type'] == 'download':
            return await self.handle_download()
        else:
            return 'invalid request'

    async def send_file(self,peer,chunking):
        reader, writer = await asyncio.open_connection(peer, 8888)
        writer.write(chunking)
        await writer.drain()
        response = await reader.read(1024)
        writer.close()
        print(response.decode())
        return response.decode()

    # if user want to upload the file
    async def handle_upload(self):
        pass
        # Chunking the file
        # send the chunking to the other peers
        # wait for their response
        # i.e the data the is uploaded need to match with the hash of chunk
        # if the hash of the chunk is matched with the hash of the data
            # response is true
        # else
            # response is false


    # if user want to download the file
    async def handle_download(self):
        pass
        # ask other peers for the file and wait for their response
        # if they have the file, they will send it to you
        # if they don't have the file, they will send you a message that they don't have the file


class HandleIncoming:
    pass