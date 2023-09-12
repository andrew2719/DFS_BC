import hashlib


class KeyGen:
    def __init__(self):
        self.data = None

    def generate_key(self, data):
        self.data = data.encode()
        hasher = hashlib.sha256(self.data)
        key = hasher.hexdigest()
        # print(key)
        return key


# # driver code
# keygen = KeyGen()
# keygen.generate_key("Hello World")