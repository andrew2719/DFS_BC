# objectives
# 1. Creating a window to browse files
# 2. Returning selected files list
# should pass 1. tkinter window, 2. number_of_files

#imports
import tkinter as tk
from tkinter import filedialog
class BrowseWindow:
    def __init__(self, browse_window, number_of_files):
        # interface
        browse_window.attributes("-topmost", True) #show on top
        self.window = browse_window
        self.number_of_files = number_of_files
        self.window.title("Browse files")  # Set title of the window
        self.window.geometry("200x70")  # Set size of the window
        self.window.config(background="white")  # Set background color of the window
        self.window.resizable(False, False)  # Prevent window from resizing

        self.browse_button = tk.Button(browse_window, text="Browse Files", command=self.browse_files)
        self.browse_button.pack(pady=20)  # Pack the button
        #interface

        self.files_list = []  # Initialize selected files list
        self.count = 0  # Initialize count to 0

    def browse_files(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.files_list.append(file_path)
            print("Selected file:", file_path)
            if len(self.files_list) == self.number_of_files:
                self.window.destroy()  # Close the window after selecting a file
        self.return_files()

    def return_files(self):
        return self.files_list

# # Driver code
# window = tk.Tk()
# browse = BrowseWindow(window,2)
# window.mainloop()

