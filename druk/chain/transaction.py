from time import time
from json import dumps


from druk.chain.key import Key
from druk.chain.hash import Hash
from druk.chain.wallet import Wallet


class Transaction:
   def __init__(self, sender, recipient, amount):
       self.timestamp = time()
       self.sender = sender
       self.recipient = recipient
       self.amount = amount
       self.hash = self.calculate_hash()
       self.signature = None


   def calculate_hash(self) -> str:
       transaction_data = {
           'timestamp': self.timestamp,
           'sender': self.sender,
           'recipient': self.recipient,
           'amount': self.amount
       }
       transaction_str = dumps(transaction_data, sort_keys=True)
       return Hash.get_hash(transaction_str)


   def sign_transaction(self, private_key) -> None:
       public_key = Key.get_public_key(private_key)
       if self.sender != public_key:
           raise Exception("You cannot sign transaction for other wallet")
       self.signature = Key.sign_transaction_hash(private_key, self.hash)


   def is_valid_transaction(self) -> bool:
       if self.sender == "network":  # Skip validation for mining rewards
           return True
       if not self.signature:
           raise Exception("No signature in this transaction")
       return Key.verify_transaction_hash(self.sender, self.signature, self.hash)


   def to_dict(self) -> dict:
       return self.__dict__


   def __repr__(self):
       return dumps(self.to_dict(), indent=2)

if __name__ == '__main__':
   wallet1 = Wallet()
   wallet2 = Wallet()


   addr1 = wallet1.public_key
   addr2 = wallet2.public_key


   tx = Transaction(addr1, addr2, 50)
   tx.sign_transaction(wallet1.private_key)


   print(tx)
