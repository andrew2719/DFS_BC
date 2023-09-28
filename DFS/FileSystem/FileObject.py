import asyncio
import aiofiles
import os
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