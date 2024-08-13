from druk.chain.block import Block
from druk.chain.chain import Chain
from druk.chain.transaction import Transaction
from druk.chain.wallet import Wallet


def test_chain():
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


   assert len(chain.blocks), 3
   assert chain.is_valid_chain()
