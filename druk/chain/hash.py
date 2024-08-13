from hashlib import sha256


class Hash:
   @staticmethod
   def get_hash(data_str) -> str:
       return sha256(data_str.encode('utf-8')).hexdigest()