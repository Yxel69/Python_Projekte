import requests
import hashlib
import time
import concurrent.futures

class Miner:
    def __init__(self, node_url, thread_count=4):
        self.node_url = node_url  # The blockchain node URL
        self.thread_count = thread_count  # Number of threads to use for mining

    def fetch_latest_block(self):
        """Fetch the latest block from the blockchain node."""
        response = requests.get(f'{self.node_url}/get_chain')
        chain = response.json()
        return chain[-1]  # Return the latest block

    def fetch_difficulty(self):
        """Fetch the current difficulty from the blockchain node."""
        response = requests.get(f'{self.node_url}/get_difficulty')
        return response.json()['difficulty']

    def calculate_hash(self, index, previous_hash, data, timestamp, nonce):
        """Calculate the block hash."""
        block_string = f"{index}{previous_hash}{data}{timestamp}{nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, previous_block, difficulty, block_data):
        """Mine a new block using multiple threads."""
        index = previous_block['index'] + 1
        previous_hash = previous_block['hash']
        timestamp = time.time()

        def try_nonce(start_nonce, step):
            """Thread worker function to try different nonces."""
            nonce = start_nonce
            while True:
                hash_value = self.calculate_hash(index, previous_hash, block_data, timestamp, nonce)
                if hash_value.startswith('0' * difficulty):
                    return nonce, hash_value
                nonce += step

        # Use thread pool to mine the block
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            futures = [executor.submit(try_nonce, i, self.thread_count) for i in range(self.thread_count)]

            # Wait for the first thread to find a valid nonce and return the result
            for future in concurrent.futures.as_completed(futures):
                nonce, hash_value = future.result()
                return {
                    "index": index,
                    "previous_hash": previous_hash,
                    "data": block_data,
                    "timestamp": timestamp,
                    "nonce": nonce,
                    "hash": hash_value
                }

    def submit_block(self, block):
        """Submit a mined block to the blockchain node."""
        response = requests.post(f'{self.node_url}/add_block', json=block)
        return response.json()

    def mine(self, block_data):
     while True:
          """Main function to handle the mining process."""
          print("Fetching latest block...")
          latest_block = self.fetch_latest_block()

          print("Fetching current difficulty...")
          difficulty = self.fetch_difficulty()

          print(f"Mining new block with difficulty {difficulty}...")
          mined_block = self.mine_block(latest_block, difficulty, block_data)

          print(f"Block mined with nonce {mined_block['nonce']}")
          print("Submitting block to the blockchain node...")
          response = self.submit_block(mined_block)

          print("Response from node:", response)

# Example of usage
if __name__ == '__main__':
    
    miner = Miner(node_url="http://localhost:5000", thread_count=8)
   
    miner.mine("New block data")
