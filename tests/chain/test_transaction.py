from druk.chain.transaction import Transaction
from druk.chain.wallet import Wallet


def test_transaction():
   wallet1 = Wallet()
   wallet2 = Wallet()


   addr1 = wallet1.public_key
   addr2 = wallet2.public_key


   tx = Transaction(addr1, addr2, 50)
   tx.sign_transaction(wallet1.private_key)


   assert tx.is_valid_transaction() == True