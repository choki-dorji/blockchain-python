from ecdsa import SECP256k1, SigningKey, VerifyingKey


class Key:
   @staticmethod
   def generate_private_key() -> str:
       signing_key = SigningKey.generate(curve=SECP256k1)
       return signing_key.to_string().hex()


   @staticmethod
   def get_public_key(private_key) -> str:
       signing_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
       verifying_key = signing_key.verifying_key
       return verifying_key.to_string().hex()


   @staticmethod
   def sign_transaction_hash(private_key, transaction_hash) -> str:
       signing_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
       signature = signing_key.sign(transaction_hash.encode('utf-8'))
       return signature.hex()


   @staticmethod
   def verify_transaction_hash(public_key, signature, transaction_hash) -> bool:
       verifying_key = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
       return verifying_key.verify(bytes.fromhex(signature), transaction_hash.encode('utf-8'))