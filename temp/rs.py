import numpy as np

# read file and store in data
fp = open(r"sample.txt", "r")
data = fp.read()
# print(data)
fp.close()

# split words and letters in data and store in data_matrix
data_matrix =  [list(word) for word in data.split()]
# print(data_matrix)

# convert data_matrix to ord values
data_matrix = [[ord(letter) for letter in word] for word in data_matrix]
print(data_matrix)

# estinmate failure rate 
