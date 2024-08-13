import asyncio
import json


from druk.p2p.payload import Payload


class Protocol:
   def __init__(self, node, reader, writer):
       self.node = node
       self.reader = reader
       self.writer = writer


   async def send(self, payload, is_recv) -> None:
       await self._send_payload(payload)
       if not is_recv:
           return
       payload = await self._recv_payload()
       if payload:
           payload_type = payload.get("type")
           addr = payload.get("addr")
           data = payload.get("data")
           if payload_type:
               if payload_type == "hello":
                   print(f"Recv 'hello' from peer on {addr['host']}:{addr['port']}")
               elif payload_type == "peers":
                   print(f"Recv 'peers' from peer on {addr['host']}:{addr['port']}")
                   await self.node.net.add_peers(data)
           else:
               print(f"Wrong payload type '{payload_type}'")
       else:
           print("Invalid payload format")


   async def recv(self) -> None:
       payload = await self._recv_payload()
       if payload:
           payload_type = payload.get("type")
           addr = payload.get("addr")
           data = payload.get("data")
           peer = (addr['host'], addr['port'])
           is_not_known_peer = self.node.net.is_not_known_peer(peer)
           if is_not_known_peer:
               await self.node.net.add_peer(peer)
               await self.broadcast_peer(addr)
           if payload_type:
               if payload_type == "hello":
                   print(f"Recv 'hello' from peer on {addr['host']}:{addr['port']}")
                   await self.send_hello()
               elif payload_type == "get_peers":
                   print(f"Recv 'get_peers' from peer on {addr['host']}:{addr['port']}")
                   await self.send_peers()
               elif payload_type == "peers":
                   print(f"Recv 'peers' from peer on {addr['host']}:{addr['port']}")
                   await self.node.net.add_peers(data)
               else:
                   print(f"Unknown payload type '{payload_type}'")
           else:
               print("Invalid payload format")


   async def broadcast_peer(self, addr):
       await asyncio.create_task(self.node.broadcast_peers([addr]))


   async def send_hello(self):
       payload = Payload.hello(self.node.get_addr(), "hello")
       await self._send_payload(payload)


   async def send_peers(self):
       peers = await self.node.net.get_peers()
       payload = Payload.peers(self.node.get_addr(), peers)
       await self._send_payload(payload)


   async def _send_payload(self, payload) -> None:
       data = json.dumps(payload).encode()
       self.writer.write(data)
       await self.writer.drain()


   async def _recv_payload(self) -> str:
       data = await self.reader.read(1024)
       return json.loads(data.decode())
