import hashlib


class KeyGen:
    def __init__(self):
        self.data = None

    def generate_key(self, data):
        self.data = data
        hasher = hashlib.sha256(self.data)
        hexer = hasher.hexdigest()
        key = bytes.fromhex(hexer)
        return key
