from druk.chain.block import Block
from druk.chain.transaction import Transaction
from druk.chain.wallet import Wallet


def test_block():
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


   assert block.is_valid_proof(4)
   assert block.has_valid_transactions()