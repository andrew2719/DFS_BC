# file chunker
import os
import time


class FolderAlreadyExistsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FileChunker:

    def __init__(self):
        self.max_chunks = 5

    def calculate_chunk_size(self, file_size):
        return (file_size + self.max_chunks - 1) // self.max_chunks

    def chunk_file(self, file_path):
        file_size = os.path.getsize(file_path)
        print(f"Uploaded file size is {file_size} KB")
        chunk_size = self.calculate_chunk_size(file_size)
        print(f"Dividing the file into 5 chunks....")
        time.sleep(1)
        try:
            if not os.path.exists("chunks"):
                os.makedirs("chunks")
            else:
                raise FolderAlreadyExistsError("chunks folder already exists")
        except FolderAlreadyExistsError as e:
            text = "-----chunks folder already exists-----"
            red = '\033[31m'
            default = '\033[0m'
            print(f"{red}{text}{default}")
            # print()
            print("chunks not created.")
            exit(0)

        print("Created a directory 'chunks'")
        with open(file_path, "rb") as file:
            chunk_id = 0
            while True:
                chunk_data = file.read(chunk_size)
                if not chunk_data:
                    break
                chunk_file_path = os.path.join("chunks", f"{chunk_id}.bin")
                with open(chunk_file_path, "wb") as chunk_file:
                    chunk_file.write(chunk_data)
                chunk_id += 1
        print("Chunks created Successfully. You can find them in the 'chunks' folder.")


# driver code
chunker = FileChunker()
chunker.chunk_file("text-file.txt")
