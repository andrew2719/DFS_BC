# file chunker
import os
from color import Color
from keygen import KeyGen


class FileChunker:
    def __init__(self):
        self.max_chunks = 5

    def calculate_chunk_size(self, file_size):
        return (file_size + self.max_chunks - 1) // self.max_chunks

    def generate_chunks(self, file_path):
        file_size = os.path.getsize(file_path)
        print(f"Uploaded file size is {file_size} KB")
        chunk_size = self.calculate_chunk_size(file_size)
        print(f"Dividing the file into {self.max_chunks} chunks....")
        if not os.path.exists("chunks"):
            os.makedirs("chunks")

        print("Created a directory 'chunks'")
        with open(file_path, "rb") as file:
            chunk_id = 1
            while True:
                chunk_data = file.read(chunk_size)
                if not chunk_data:
                    break
                chunk_file_path = os.path.join("chunks", f"{chunk_id}.bin")
                with open(chunk_file_path, "wb") as chunk_file:
                    chunk_file.write(chunk_data)
                chunk_id += 1
        print(f"{Color.green}Chunks created Successfully. You can find them in the 'chunks' folder.{Color.default}")

# # driver code
# chunker = FileChunker()
# chunker.generate_chunks("pdf-file.pdf")
