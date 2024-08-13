from time import time
from json import dumps


from druk.chain.hash import Hash
from druk.chain.transaction import Transaction
from druk.chain.wallet import Wallet


class Block:
   def __init__(self, index, transactions, previous_hash, nonce=0):
       self.index = index
       self.timestamp = time()
       self.transactions = transactions
       self.previous_hash = previous_hash
       self.nonce = nonce
       self.hash = self.compute_hash()


   def compute_hash(self) -> str:
       block_data = {
           'index': self.index,
           'timestamp': self.timestamp,
           'transactions': [tx.hash for tx in self.transactions],
           'previous_hash': self.previous_hash,
           'nonce': self.nonce
       }
       transaction_str = dumps(block_data, sort_keys=True)
       return Hash.get_hash(transaction_str)


   def mine_block(self, difficulty) -> None:
       while self.hash[0:difficulty] != '0' * difficulty:
           self.nonce += 1
           self.hash = self.compute_hash()


   def is_valid_proof(self, difficulty) -> bool:
       return (self.hash.startswith('0' * difficulty)
               and self.hash == self.compute_hash())


   def has_valid_transactions(self) -> bool:
       for tx in self.transactions:
           if not tx.is_valid_transaction():
               return False
       return True


   def to_dict(self) -> dict:
       return {
           'index': self.index,
           'timestamp': self.timestamp,
           'transactions': [tx.to_dict() for tx in self.transactions],
           'previous_hash': self.previous_hash,
           'nonce': self.nonce,
           'hash': self.hash
       }


   def __repr__(self):
       return dumps(self.to_dict(), indent=2)
   
if __name__ == '__main__':
   wallet1 = Wallet()
   wallet2 = Wallet()


   addr1 = wallet1.public_key
   addr2 = wallet2.public_key


   tx1 = Transaction(addr1, addr2, 50)
   tx2 = Transaction(addr2, addr1, 30)


   tx1.sign_transaction(wallet1.private_key)
   tx2.sign_transaction(wallet2.private_key)


   block = Block(1, [tx1, tx2], "0" * 64)
   block.mine_block(4)


   print(block)
