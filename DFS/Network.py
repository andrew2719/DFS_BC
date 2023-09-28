import asyncio
import os

class Network:

    def __init__(self, port, peers=[], save_path='./received_files'):
        self.port = port
        self.peers = peers
        self.peer_connections = {}
        self.save_path = save_path

        if not os.path.exists(save_path):
            os.makedirs(save_path)