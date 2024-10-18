import os
import json
import atexit
from flask import Flask, request, jsonify
import hashlib
import time

app = Flask(__name__)

class Block:
    def __init__(self, index, previous_hash, data, timestamp=None, nonce=0, hash=''):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = hash

    def to_dict(self):
        """Converts the block object to a dictionary for JSON serialization."""
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'data': self.data,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash
        }

    @staticmethod
    def from_dict(data):
        """Creates a Block object from a dictionary."""
        return Block(
            index=data['index'],
            previous_hash=data['previous_hash'],
            data=data['data'],
            timestamp=data['timestamp'],
            nonce=data['nonce'],
            hash=data['hash']
        )


class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4  # Starting difficulty
        self.target_block_time = 60  # Target block time in seconds (1 minute)
        self.adjustment_interval = 5  # Adjust difficulty after every 5 blocks
        self.block_times = []  # List to store block mining times

        # Load blockchain if it exists
        self.load_chain()

        # If the chain is empty, create the genesis block
        if not self.chain:
            self.chain.append(self.create_genesis_block())

    def create_genesis_block(self):
        """Creates the first block (Genesis Block)."""
        return Block(0, "0", "Genesis Block", time.time(), 0, self.calculate_hash(0, "0", "Genesis Block", time.time(), 0))

    def calculate_hash(self, index, previous_hash, data, timestamp, nonce):
        """Calculates the hash of the block."""
        block_string = f"{index}{previous_hash}{data}{timestamp}{nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_block(self, new_block):
        """Adds a block to the blockchain and adjusts difficulty if necessary."""
        if self.is_valid_block(new_block, self.chain[-1]):
            self.chain.append(new_block)
            self.track_block_time(new_block.timestamp)

            # Adjust difficulty every `adjustment_interval` blocks
            if len(self.chain) % self.adjustment_interval == 0:
                self.adjust_difficulty()

            return True
        return False

    def track_block_time(self, new_timestamp):
        """Tracks the time taken to mine the last blocks."""
        if len(self.block_times) == self.adjustment_interval:
            self.block_times.pop(0)  # Remove the oldest block time

        # Ensure there's a previous block to compare to
        if len(self.chain) > 1:
            last_block_time = self.chain[-2].timestamp  # Get the timestamp of the second last block
            time_diff = new_timestamp - last_block_time
            self.block_times.append(time_diff)

    def adjust_difficulty(self):
        """Adjusts the difficulty based on the time taken to mine the last 5 blocks."""
        if len(self.block_times) < self.adjustment_interval:
            return  # Wait until we have enough blocks to adjust

        avg_block_time = sum(self.block_times) / len(self.block_times)

        if avg_block_time > self.target_block_time:
            self.difficulty = max(1, self.difficulty - 1)  # Ensure difficulty doesn't go below 1
        elif avg_block_time < self.target_block_time:
            self.difficulty += 1

    def is_valid_block(self, new_block, previous_block):
        """Validate a new block before adding it."""
        if previous_block.index + 1 != new_block.index:
            return False
        if previous_block.hash != new_block.previous_hash:
            return False
        if new_block.hash != self.calculate_hash(new_block.index, new_block.previous_hash, new_block.data, new_block.timestamp, new_block.nonce):
            return False
        return True

    def get_chain(self):
        """Return the full blockchain as a list."""
        return [block.to_dict() for block in self.chain]

    def save_chain(self):
        """Saves the blockchain to a file."""
        with open('blockchain.json', 'w') as f:
            json.dump(self.get_chain(), f)

    def load_chain(self):
        """Loads the blockchain from a file."""
        if os.path.exists('blockchain.json'):
            with open('blockchain.json', 'r') as f:
                chain_data = json.load(f)
                self.chain = [Block.from_dict(block_data) for block_data in chain_data]

    def get_difficulty(self):
        """Return the current difficulty level."""
        return self.difficulty


blockchain = Blockchain()

# Save blockchain to file when the program exits
atexit.register(blockchain.save_chain)

@app.route('/add_block', methods=['POST'])
def add_block():
    block_data = request.get_json()
    block = Block(block_data['index'],
                  block_data['previous_hash'],
                  block_data['data'],
                  block_data['timestamp'],
                  block_data['nonce'],
                  block_data['hash'])
    
    if blockchain.add_block(block):
        return jsonify({"message": "Block added successfully", "chain": blockchain.get_chain()}), 201
    else:
        return jsonify({"message": "Block is invalid"}), 400

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain.get_chain()), 200

@app.route('/get_difficulty', methods=['GET'])
def get_difficulty():
    return jsonify({"difficulty": blockchain.get_difficulty()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
