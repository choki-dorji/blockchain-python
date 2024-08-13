from json import dumps


from druk.chain.block import Block
from druk.chain.transaction import Transaction
from druk.chain.wallet import Wallet


class Chain:
   def __init__(self, difficulty, reward):
       self.difficulty = difficulty
       self.reward = reward
       self.blocks = [self.create_genesis_block()]


   def create_genesis_block(self) -> Block:
       return Block(0, [], "0" * 64)


   def get_latest_block(self) -> Block:
       return self.blocks[-1]


   def add_block(self, block) -> bool:
       if self.is_valid_block(block):
           self.blocks.append(block)
           return True
       return False


   def is_valid_block(self, block) -> bool:
       if block.previous_hash != self.get_latest_block().hash:
           return False
       if not block.is_valid_proof(self.difficulty):
           return False
       if not block.has_valid_transactions():
           return False
       return True


   def is_valid_chain(self) -> bool:
       for i in range(1, len(self.blocks)):
           curr_block = self.blocks[i]
           prev_block = self.blocks[i - 1]
           if curr_block.previous_hash != prev_block.hash:
               return False
           if not curr_block.is_valid_proof(self.difficulty):
               return False
           if not curr_block.has_valid_transactions():
               return False
       return True


   def to_dict(self) -> dict:
       return {
           'difficulty': self.difficulty,
           'reward': self.reward,
           'blocks': [block.to_dict() for block in self.blocks]
       }


   def __repr__(self):
       return dumps(self.to_dict(), indent=2)

if __name__ == '__main__':
   wallet1 = Wallet()
   wallet2 = Wallet()
   wallet3 = Wallet()


   addr1 = wallet1.public_key
   addr2 = wallet2.public_key
   addr3 = wallet2.public_key


   tx1 = Transaction(addr1, addr2, 50)
   tx2 = Transaction(addr2, addr3, 30)
   tx3 = Transaction(addr3, addr1, 10)


   tx1.sign_transaction(wallet1.private_key)
   tx2.sign_transaction(wallet2.private_key)
   tx3.sign_transaction(wallet3.private_key)


   chain = Chain(4, 100)


   block1 = Block(1, [tx1, tx2], chain.get_latest_block().hash)
   block1.mine_block(chain.difficulty)
   chain.add_block(block1)


   block2 = Block(2, [tx3], chain.get_latest_block().hash)
   block2.mine_block(chain.difficulty)
   chain.add_block(block2)


   print(chain)
