import hashlib


class Chunker:
    def __init__(self,file_obj):
        self.file_obj = file_obj
    async def chunk_file(self, num_chunks=8):
        data = self.file_obj.data
        chunk_table = {}
        chunk_size = len(data) // num_chunks
        end_index = 0
        for i in range(num_chunks):
            start_index = i * chunk_size
            end_index = start_index + chunk_size
            chunk = data[start_index:end_index]
            sha256 = hashlib.sha256(chunk).hexdigest()
            chunk_table[i] = {
                'index': i,
                'hash': sha256,
                'data': chunk,
                'size': chunk_size,
                'sent': False,
                'peer': None
            }

        # If there's remaining data, add it as an extra chunk
        if len(data) % num_chunks != 0:
            extra_chunk = data[end_index:]
            sha256 = hashlib.sha256(extra_chunk).hexdigest()
            chunk_table[num_chunks] = {
                'index': num_chunks,
                'hash': sha256,
                'data': extra_chunk,
                'size': len(extra_chunk),
                'sent': False,
                'peer': None
            }

        return chunk_table

    async def regenerate_file(self, chunk_table):
        # Sort the chunk_table by index
        sorted_chunk_table = sorted(chunk_table, key=lambda x: x['index'])

        # Concatenate the chunks back together
        original_data = b"".join([chunk['data'] for chunk in sorted_chunk_table])

        return original_data