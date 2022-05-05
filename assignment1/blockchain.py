#Function imports

import hashlib
import json

class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def format_string(self) -> str:
        _format_string = "{0} sends {1} {2} bitcoin.".format(self.sender, self.receiver, self.amount) 
        return _format_string


class Block:
    def __init__(self, prev_hash: str, transactions: list, index: int):
        self.prev_hash = prev_hash
        # I originally thought that a block might contain more than 1 transaction
        # so I implemented it as a list.
        # Seems like it should just be of length 1
        self.transactions = transactions
        self.nonce = 1
        self.index = index
        self.hash = self.compute_hash()

    def format_print(self):
        format_string = "Block at index {0}:\n".format(self.index)
        format_string += "  Nonce: {0}\n".format(self.nonce)
        format_string += "  Previous hash: {0}\n".format(self.prev_hash)
        format_string += "  Current hash : {0}\n".format(self.hash)
        format_string += "  Transaction  : {0}\n".format(self.transactions[0].format_string())
        print(format_string)

    def compute_hash(self) -> str:
        transactions_str = list(map((lambda t: t.format_string()), self.transactions))
        block_content = self.prev_hash + "".join(transactions_str) + str(self.nonce)
        return hashlib.sha256(block_content.encode('UTF-8')).hexdigest()

    def proof_of_work(self):
        """
        Perform proof of work to validate transaction and add transaction to chain. Essentially mine the transaction
        """
        # Difficulty is set to 4 in accordance with webpage
        while not self.compute_hash().startswith("0000"):
            self.nonce += 1
        self.hash = self.compute_hash()
        print("Block mined! Current hash: {0}".format(self.hash))


class Blockchain:
    def __init__(self):
        # initialize empty chain to store blocks
        self.current_index = 0
        self.transaction_pool = []
        self.chain = [self.new_genesis_block()]

    def new_genesis_block(self) -> Block:
        initial_transac = Transaction("Genesis", "Genesis", 0)
        genesis = Block("0"*64, [initial_transac], 0)
        genesis.proof_of_work()
        self.current_index += 1
        return genesis

    def get_last_block(self) -> Block:
        return self.chain[-1]


    def new_block(self):
        """
        Create a New block for a transaction here
        """
        transaction = self.transaction_pool[0]
        block = Block(self.get_last_block().hash, [transaction], self.current_index)
        block.proof_of_work()
        self.chain.append(block)
        self.current_index += 1
        self.transaction_pool = []

    def new_transaction(self, sender, receiver, amount):
        """
        Define a transaction between users here
        """
        transaction = Transaction(sender, receiver, amount)
        self.transaction_pool.append(transaction)

    def format_print(self):
        for i in range(len(self.chain)):
            self.chain[i].format_print()

if __name__ == "__main__":
    # Define the Blockchain
    my_blockchain = Blockchain()
    
    # Define a transaction
    my_blockchain.new_transaction("Alice", "Bob", 1)

    # Validate transaction and add to blockchain
    my_blockchain.new_block()
    
    # Repeat to get 5 entries
    my_blockchain.new_transaction("Bob", "Chad", 2)
    my_blockchain.new_block()
    my_blockchain.new_transaction("Chad", "Dan", 3)
    my_blockchain.new_block()
    my_blockchain.new_transaction("Dan", "Erin", 4)
    my_blockchain.new_block()
    my_blockchain.new_transaction("Erin", "Frank", 5)
    my_blockchain.new_block()

    # Display the blockchain
    my_blockchain.format_print()

    

    