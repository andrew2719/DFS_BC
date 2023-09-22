import asyncio
import aiofiles
import chunker

class PeerHandler:
    def __init__(self,peer_connections,file_obj):
        self.peer_connections = peer_connections
        self.file_obj = file_obj
        self.chunk_table = chunker.Chunker(file_obj).chunk_file()

    async def UploadToPeer(self):
        pass
    async def UploadToPeers(self):
        pass