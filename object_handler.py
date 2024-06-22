from npc import NPC
from sprite_object import *

class ObjectHandler:
  def __init__(self, game) -> None:
    self.game = game
    self.sprite_list = []
    self.npc_list = []
    self.npcs = {}
    self.npc_sprite_path = 'ressources/sprites/npc'
    self.static_sprite_path = 'ressources/sprites/static sprites'
    self.animated_sprite_path = 'ressources/sprites/animated sprites'
    add_sprite = self.add_sprite
    # add_npc = self.add_npc

    add_sprite(AnimatedSprite(game))
    add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
    add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
    add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
    add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
    add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
    add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
    add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
    add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
    add_sprite(AnimatedSprite(game, pos=(14.5, 5.5)))
    add_sprite(AnimatedSprite(game, pos=(14.5, 7.5)))
    add_sprite(AnimatedSprite(game, pos=(12.5, 7.5)))
    add_sprite(AnimatedSprite(game, pos=(9.5, 7.5)))
    add_sprite(AnimatedSprite(game, pos=(14.5, 12.5)))
    add_sprite(AnimatedSprite(game, pos=(9.5, 20.5)))
    add_sprite(AnimatedSprite(game, pos=(10.5, 20.5)))
    add_sprite(AnimatedSprite(game, pos=(3.5, 14.5)))
    add_sprite(AnimatedSprite(game, pos=(3.5, 18.5)))
    add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
    add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
    add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
    add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

    # add_npc(NPC(game))

  def update(self):
    [sprite.update() for sprite in self.sprite_list]
    [npc.update() for npc in self.npc_list]
    

  def add_npc(self, npc: NPC, player_name: str):
    self.npc_list.append(npc)
    self.npcs[player_name] = npc

  def add_sprite(self, sprite):
    self.sprite_list.append(sprite)