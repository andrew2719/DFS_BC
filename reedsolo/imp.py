#imports
import os
import reedsolo

# read file
with open('data.pdf', 'rb') as myfile:
    data=myfile.read()
print(data)

# encode data
rs = reedsolo.RSCodec(2) # 2 error correction bytes
