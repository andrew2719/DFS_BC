# file regenerator
import os
from color import Color


class FileRegenerator:
    def __init__(self, folder_path):
        if os.path.exists("chunks"):
            self.chunk_folder = folder_path

    def regenerate_file(self, output_file):
        print("regenerating the files using chunks...")
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
        print(f"{Color.green}file regenerated successfully. You can find '{output_file}'{Color.default}")


# # driver code
#
# regenerator = FileRegenerator()
# regenerator.regenerate_file('regenerated.pdf')
