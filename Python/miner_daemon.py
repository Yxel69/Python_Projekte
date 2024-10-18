import hashlib
import time
import requests

class Block:
    def __init__(self, index, previous_hash, data, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        """Mine the block using Proof of Work."""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

def get_latest_block():
    """Fetch the latest block from the node."""
    response = requests.get("http://localhost:5000/get_chain")
    chain = response.json()
    return chain[-1]  # Return the latest block in the chain

def get_current_difficulty():
    """Fetch the current difficulty from the node."""
    response = requests.get("http://localhost:5000/get_difficulty")
    return response.json()["difficulty"]

def mine_block():
    """Mine a new block every minute, adjusting difficulty based on the node."""
    while True:
        latest_block = get_latest_block()
        new_index = latest_block['index'] + 1
        previous_hash = latest_block['hash']
        data = {"transactions": f"Block {new_index} mined"}  # Add your block data (e.g., transactions)
        timestamp = time.time()

        # Fetch the current difficulty from the node
        difficulty = get_current_difficulty()
        print(f"Current mining difficulty: {difficulty}")

        # Create a new block
        new_block = Block(new_index, previous_hash, data, timestamp)
        
        # Mine the block
        new_block.mine_block(difficulty)

        # Send the block to the node daemon
        block_data = {
            "index": new_block.index,
            "previous_hash": new_block.previous_hash,
            "data": new_block.data,
            "timestamp": new_block.timestamp,
            "nonce": new_block.nonce,
            "hash": new_block.hash
        }

        response = requests.post("http://localhost:5000/add_block", json=block_data)
        if response.status_code == 201:
            print(f"Block {new_block.index} successfully added to the blockchain.")
        else:
            print(f"Failed to add block {new_block.index}: {response.json()['message']}")


if __name__ == '__main__':
    mine_block()
