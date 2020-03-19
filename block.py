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
        :param block
        :return: the hash of the block instance by converting it into a JSON string
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:

    def __init__(self):
        """
        Constructor for the Blockchain class
        """
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