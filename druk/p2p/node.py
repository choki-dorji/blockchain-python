import asyncio


from druk.p2p.constants import (
   MAX_PEERS,
   SAVE_PEERS_INTERVAL,
)
from druk.p2p.payload import Payload
from druk.p2p.net import Net
from druk.p2p.protocol import Protocol


class Node:
   def __init__(self, host, port, max_peers=MAX_PEERS):
       self.host = host
       self.port = port
       self.net = Net(self, max_peers)


   async def run(self) -> None:
       # load & save net peers
       self.net.load_peers()
       asyncio.create_task(self.save_peers_periodically())


       # start server
       server = await asyncio.start_server(self._recv_from_peer, self.host, self.port)
       print(f"Node listen on {self.host}:{self.port}")


       # create tasks on startup
       await asyncio.create_task(self.broadcast_hello())
       await asyncio.create_task(self.broadcast_get_peers())


       # server run forever
       async with server:
           await server.serve_forever()


   async def save_peers_periodically(self):
       while True:
           await asyncio.sleep(SAVE_PEERS_INTERVAL)
           await self.net.save_peers()


   async def broadcast_hello(self):
       payload = Payload.hello(self.get_addr(), "hello")
       await self._broadcast_to_peers(payload)


   async def broadcast_get_peers(self):
       payload = Payload.get_peers(self.get_addr(), "")
       await self._broadcast_to_peers(payload)


   async def broadcast_peers(self, peers_data):
       payload = Payload.peers(self.get_addr(), peers_data)
       await self._broadcast_to_peers(payload, False)


   async def _broadcast_to_peers(self, payload, is_recv=True):
       peers = self.net.get_gossip_peers()
       while len(peers) > 0:
           peer = peers.pop()
           is_success = await self._send_to_peer(peer[0], peer[1], payload, is_recv)
           if not is_success:
               await self.net.remove_peer((peer[0], peer[1]))


   async def _send_to_peer(self, host, port, payload, is_recv) -> bool:
       try:
           reader, writer = await asyncio.open_connection(host, port)
           protocol = Protocol(self, reader, writer)
           await protocol.send(payload, is_recv)
           writer.close()
           await writer.wait_closed()
           return True
       except OSError:
           print(f"Failed to connect to peer on {host}:{port}")
           return False


   async def _recv_from_peer(self, reader, writer) -> None:
       protocol = Protocol(self, reader, writer)
       await protocol.recv()
       writer.close()
       await writer.wait_closed()


   def get_addr(self) -> dict:
       return {
           "host": self.host,
           "port": self.port
       }


async def start_node(host, port) -> None:
   server = Node(host, port)
   await server.run()




if __name__ == "__main__":
   asyncio.run(start_node("localhost", 5000))
