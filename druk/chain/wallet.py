from druk.chain.key import Key


class Wallet:
   def __init__(self, private_key=Key.generate_private_key()):
       self.private_key = private_key
       self.public_key = Key.get_public_key(private_key)


   def sign_transaction_hash(self, transaction_hash) -> str:
       return Key.sign_transaction_hash(self.private_key, transaction_hash)