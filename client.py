import socket, pickle
from npc import NPC
from settings import *

class Client:
  def __init__(self, game) -> None:
    self.game = game
    self.object_handler = self.game.object_handler
    self.get_connected()

  def get_connected(self):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def update(self):
    self.send_coordinates()

  def draw(self):
    msg = self.recv_message()
    
    for player, data in msg.items():
      if player != self.game.player.name:
        x, y, angle = data.split(',')
        if player not in self.object_handler.npcs:
          self.game.object_handler.npc_list.append(NPC(self.game))
          self.game.object_handler.npcs[player] = NPC(self.game)
          print(f'{player} is connected as {self.game.object_handler.npcs[player]}')
        else:
          # self.game.object_handler.npcs[player].x = float(x)
          # self.game.object_handler.npcs[player].y = float(y)
          self.game.object_handler.npcs[player].pos = (float(x), float(y))
          # self.game.object_handler.npcs[player].mouvement((float(x), float(y)), float(angle))
          self.game.object_handler.npcs[player].angle = float(angle) 
          # # could change to float later
          self.game.object_handler.npcs[player].update()
          
  def send_msg(self, msg: bytes):
    msg += b' ' * (HEADER - len(msg))
    self.client.sendto(msg, ADDR)

  def send_coordinates(self):
    self.data = f'{self.game.player.x},{self.game.player.y},{self.game.player.name},{self.game.player.angle}'
    self.send_msg(pickle.dumps(self.data))

  def recv_message(self) -> dict:
    msg = pickle.loads(self.client.recvfrom(HEADER)[0])
    if msg:
      return msg

  def disconnect(self):
    # print(self.game.player.name)
    # self.game.object_handler.npcs.pop(self.game.player.name)
    self.send_msg(pickle.dumps(f'{DM}:{self.game.player.name}'))