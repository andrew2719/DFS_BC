import asyncio
import aiofiles
from . import Json_handler
from DFS.FileSystem import FileObject
from DFS.logger import logger
class Handler:
    # handles the incoming requests
    def __init__(self, reader, writer,request):
        self.REQUEST = request
        self.file_info = None
        self.reader = reader
        self.writer = writer

    async def HandleUpload(self):
        pass

    async def HandleDownload(self):
        pass