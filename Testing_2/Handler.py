import asyncio
import aiofiles
import os
import json
import hashlib

class FileObject:
    def __init__(self, file_name, file_size):
        self.file_name = file_name
        self.file_size = file_size
        self.data = bytearray() #this can store the chunks of data
        self.hasher = hashlib.sha256()

    def append_data(self, chunk):
        self.data.extend(chunk)
        self.hasher.update(chunk)

class Handle:
    def __init__(self,file_info,reader,writer):
        self.file_info = file_info
        self.reader = reader
        self.writer = writer
        self.file_obj = FileObject(file_info["file_name"], file_info["file_size"])

    async def HandleUpload(self):
        print(self.file_info)
        file_name = self.file_info['file_name']
        file_size = self.file_info['file_size']
        size = 0
        while size < file_size:
            chunk = await self.reader.read(1024)
            size += len(chunk)
            self.file_obj.append_data(chunk)  # Append data to FileObject

            if size >= file_size or chunk == b'':
                break

        return self.file_obj
    async def HandleDownload(self):
        pass