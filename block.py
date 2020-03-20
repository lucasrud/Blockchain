from hashlib import sha256
import time
import json


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        """
        Constructor for a 'Block'
        :param index: Unique ID
        :param transactions: list of transactions
        :param timestamp: Time of generation of the Block
        :param previous_hash: Hash of the previous block in the chain
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def compute_hash(self):
        """
        :return: the hash of the block instance by converting it into a JSON string
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:

    # difficulty of the proof of work algorithm
    difficulty = 2

    def __init__(self):
        """
        Constructor for the Blockchain class
        """
        self.unconfirmed_transactions = [] # data yet to get into the blockchain
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Generates the genesis block and appends it to the chain.
        index = 0, previous_hash = 0, and a valid hash
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """
        A quick way to retrieve the most recent block in the chain. Note that
        the chain will always consist of at least one block (i.e., genesis block)
        """
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        A simplified version of the Hashcash Algorithm used in Bitcoin
        Tries different values of the nonce to get a hash that fits our difficulty criteria
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0', * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash


    def add_block(self, block, proof):
        """
        Adds the block to the chain after successful verification
        Verification:
        * Check if the proof is valid
        * The previous_hash matches the hash of the last block in the chain
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisifes the difficulty criteria.
        """
        return block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash()

    def add_new_transaction(self, transaction):
        self.uncomfirmed_transactions.append(transaction)

    def mine(self):
        """
        An interface to add pending transactions to the blockchain by adding them to the block and computing proof of work
        """
        if not self.uncomfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block + 1, transactions=self.uncomfirmed_transactions, timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
