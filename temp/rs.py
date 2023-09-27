import numpy as np

with open(r"sample.txt", "r") as fp:
    data = fp.read()

words = data.split()
letters = [list(word) for word in words]
ords = [[ord(letter) for letter in word] for word in words]
ords = np.array(ords,dtype=int)

print(ords)


