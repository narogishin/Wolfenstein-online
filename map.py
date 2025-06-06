import pygame as pg
from settings import RATIO

_ = False
mini_map = [
  [1,1,1,1,1,7,1,1,1,1,1,1,1,1,1,1],
  [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
  [1,_,_,1,1,1,1,_,_,_,2,2,2,_,_,1],
  [1,_,_,_,_,_,1,_,_,_,_,_,2,_,_,1],
  [1,_,_,_,_,_,1,_,_,_,_,_,2,_,_,1],
  [1,_,_,1,1,1,1,_,_,_,_,_,_,_,_,1],
  [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
  [1,_,_,1,_,_,_,1,_,_,_,_,_,_,_,1],
  [1,1,1,1,1,5,1,1,1,1,1,5,1,1,1,1],
]

class Map:
  def __init__(self, game) -> None:
    self.game = game
    self.mini_map = mini_map
    self.world_map = {}
    self.get_map()

  def get_map(self):
    for j, row in enumerate(self.mini_map):
      for i, value in enumerate(row):
        if value:
          self.world_map[(i, j)] = value

  def draw(self):
    [pg.draw.rect(self.game.screen, 'darkgray', (pos[0]*100*RATIO, pos[1]*100*RATIO, 100*RATIO, 100*RATIO), 2) 
     for pos in self.world_map]