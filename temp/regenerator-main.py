from color import Color
from file_regenerator import FileRegenerator

folder_path = input("Enter the path of the folder containing the chunks: ")
output_file = input("Enter the name of the output file with extension: ")

regenerator = FileRegenerator(folder_path)
regenerator.regenerate_file(output_file)
