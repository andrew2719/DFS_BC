import json
import chunker


class PeerHandler:
    def __init__(self, peer_connections, file_obj):
        self.peer_connections = peer_connections
        self.file_obj = file_obj
        self.chunker = chunker.Chunker(file_obj)
        self.chunk_table = None


    async def generate_chunk_table(self):
        self.chunk_table = await self.chunker.chunk_file()
        '''chunk_table[i] = {
                'index': i,
                'hash': sha256,
                'data': chunk,
                'size': chunk_size,
                'sent': False,
                'peer': None
            }
        '''

    async def UploadToPeer(self, peer, chunk):
        reader, writer = self.peer_connections[peer]

        # Preparing the file info for sending to the peer
        file_info = {
            "REQUEST": "UPLOAD",
            "NODE": "NODE",
            "file_name": chunk['hash'],
            "file_size": chunk['size']
        }

        # Send the file info as JSON
        writer.write(json.dumps(file_info).encode())
        await writer.drain()

        # Send the chunk data
        writer.write(chunk['data'])
        await writer.drain()

        # Read acknowledgment from the peer
        ack_data = await reader.read(1024)
        ack = json.loads(ack_data.decode())

        return (peer, ack['status'])

    async def UploadToPeers(self):
        if self.chunk_table is None:
            await self.generate_chunk_table()

        for i in self.chunk_table:
            chunk = self.chunk_table[i]
            peer = self.select_peer_for_chunk(i)
            self.chunk_table[i]['peer'] = peer
            peer, status = await self.UploadToPeer(peer, chunk)
            if status == 'success':
                self.chunk_table[i]['sent'] = True
            else:
                self.chunk_table[i]['sent'] = False


    def select_peer_for_chunk(self, chunk_index):
        # Logic to decide which peer receives which chunk
        peer_keys = list(self.peer_connections.keys())
        selected_peer = peer_keys[chunk_index % len(peer_keys)]
        return selected_peer

