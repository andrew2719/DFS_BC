# total control
from color import Color
from browse import BrowseWindow
from file_chunker import FileChunker

import tkinter as tk


# taking file input
try:
    number_of_files = int(input("Enter the number of files to be uploaded: "))
except ValueError:
    print(f"{Color.red}Please enter a valid number.{Color.default}")
    exit(0)
window = tk.Tk()
browse = BrowseWindow(window, number_of_files)
files_list = browse.return_files()
window.mainloop() # infinite loop to keep the window open
print()
print("Selected files:")
print(f"*files_list", sep="\n")
print()


# dividing the files into chunks

chunker = FileChunker()
for file in files_list:
    chunker.generate_chunks(file)
print()
