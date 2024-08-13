import asyncio
import json
import random


from druk.p2p.constants import SEED_PEERS


class Net:
   def __init__(self, node, max_peers):
       self.node = node
       self.max_peers = max_peers
       self.peers_file = f"peers_{node.port}.json"
       self.peers_lock = asyncio.Lock()
       self.peers = set()


   def get_gossip_peers(self):
       peers = list(self.peers)
       if len(peers) <= self.max_peers:
           return peers
       return random.sample(peers, self.max_peers)


   async def add_peers(self, peers_data):
       for peer_item in peers_data:
           peer = (peer_item["host"], peer_item["port"])
           if self.is_not_me_peer(peer):
               await self.add_peer(peer)


   async def get_peers(self):
       peers = [
           {
               "host": peer[0],
               "port": peer[1]
           } for peer in self.peers
       ]
       return peers


   async def add_peer(self, peer) -> None:
       async with self.peers_lock:
           self.peers.add(peer)


   async def remove_peer(self, peer) -> None:
       async with self.peers_lock:
           self.peers.discard(peer)


   def is_not_me_peer(self, peer) -> bool:
       return peer != (self.node.host, self.node.port)


   def is_not_known_peer(self, peer) -> bool:
       return peer not in self.peers


   def load_peers(self) -> None:
       try:
           with open(self.peers_file, "r") as f:
               peers = json.load(f)
               self.peers = set(
                   (peer['host'], peer['port']) for peer in peers)
       except FileNotFoundError:
           self.peers = set(
               peer for peer in SEED_PEERS if self.is_not_me_peer(peer))


   async def save_peers(self) -> None:
       peers = await self.get_peers()
       with open(self.peers_file, "w") as f:
           json.dump(peers, f, indent=2)
