import hashlib
import json
from time import time
from uuid import uuid4
from typing import Dict, List, Optional, Union

Transaction = Dict[str, Union[int, str]]
CurrentTransactions = List[Transaction]
Block = Dict[str, Union[int, float, CurrentTransactions, str, None]]

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof: int, previous_hash: str=None) -> Block:
        # Creates a new Block and adds it to the chain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block


    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        # Adds a new transaction to the list of transactions
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1


    @staticmethod
    def hash(block: Block) -> str:
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self) -> Block:
        # Returns the last Block in the chain
        return self.chain[-1]


    def proof_of_work(self, last_proof: int) -> int:
        # Simple Proof of Work Algorithm
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
             proof += 1
        return proof


    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        # Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        guess = '{lp}{p}'.format(lp=last_proof, p=proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# print(Blockchain.new_block.__annotations__)

