#imports
import os
import reedsolo

# read file
with open('data.pdf', 'rb') as myfile:
    data=myfile.read()
print(data)
print()
# encode data
rs = reedsolo.RSCodec(222) # 2 error correction bytes
print("--------------------------------")
encoded_data = rs.encode(data) # encode method takes bytes as input
print("Encoded Data:", encoded_data)

# add corruption to encoded data
corrupted_data = bytearray(encoded_data)
corrupted_data[4] = 00 # Introducing an error by modifying a byte.
print("Corrupted Data:", corrupted_data)

# decode corrupted data
try:
    decoded_data = rs.decode(corrupted_data)
    print("Corrected Data:", decoded_data[0].decode())
except ValueError:
    print("Failed to correct data. Too many errors.")
