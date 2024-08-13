class Payload:
#    address means the address of current node bdefore sending
   @staticmethod
   def hello(addr, hello_data):
       return Payload._payload("hello", addr, hello_data)


   @staticmethod
   def status(addr, status_data):
       return Payload._payload("status", addr, status_data)


   @staticmethod
   def ping(addr, ping_data):
       return Payload._payload("ping", addr, ping_data)


   @staticmethod
   def pong(addr, pong_data):
       return Payload._payload("pong", addr, pong_data)


   @staticmethod
   def disconnect(addr, disconnect_data):
       return Payload._payload("disconnect", addr, disconnect_data)


   @staticmethod
   def get_peers(addr, get_peers_data):
       return Payload._payload("get_peers", addr, get_peers_data)


   @staticmethod
   def peers(addr, peers_data):
       return Payload._payload("peers", addr, peers_data)


   @staticmethod
   def get_transactions(addr, get_transactions_data):
       return Payload._payload("get_transactions", addr, get_transactions_data)


   @staticmethod
   def transactions(addr, transactions_data):
       return Payload._payload("transactions", addr, transactions_data)


   @staticmethod
   def get_blocks(addr, get_blocks_data):
       return Payload._payload("get_blocks", addr, get_blocks_data)


   @staticmethod
   def blocks(addr, blocks_data):
       return Payload._payload("blocks", addr, blocks_data)


   @staticmethod
   def _payload(payload_type, addr, data):
       payload = {
           "type": payload_type,
           "addr": addr,
           "data": data
       }
       return payload
