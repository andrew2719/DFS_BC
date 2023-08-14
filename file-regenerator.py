# file regenerator
import os
import time


class Color:
    red = '\033[31m'
    green = '\033[32m'
    default = '\033[0m'


class FolderNotExistsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FileRegenerator:
    def __init__(self):
        try:
            if os.path.exists("chunks"):
                self.chunk_folder = 'chunks'
            else:
                raise FolderNotExistsError("chunks folder doesn't exist")
        except FolderNotExistsError:
            print(f"{Color.red} ---chunks folder doesn't exist--- {Color.default}")
            print("file regeneration failed.")
            exit(0)

    def regenerate(self, output_file):
        print("regenerating the files using chunks...")
        time.sleep(1)
        with open(output_file, 'wb') as output:
            chunk_id = 1
            while True:
                chunk_file_path = os.path.join(f'{self.chunk_folder}', f"{chunk_id}.bin")
                if not os.path.exists(chunk_file_path):
                    break
                with open(chunk_file_path, 'rb') as chunk_file:
                    temp = chunk_file.read()
                    output.write(temp)
                chunk_id += 1
        print(f"{Color.green}file regenerated successfully. You can find 'regenerated.txt'{Color.default}")


# driver code

regenerator = FileRegenerator()
regenerator.regenerate('regenerated.txt')
