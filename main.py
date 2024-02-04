import pygame as pg
import sys
from object_handler import ObjectHandler
from settings import RESOLUTION, FPS
from map import Map
from player import Player
from ray_casting import RayCasting
from object_renderer import ObjectRenderer
from sprite_object import SpriteObject

class Game:
  def __init__(self) -> None:
    pg.init()
    pg.mouse.set_visible(False)
    self.screen = pg.display.set_mode(RESOLUTION)
    self.clock = pg.time.Clock()
    self.dt = 1
    self.new_game()

  def new_game(self):
   self.map = Map(self)
   self.player = Player(self)
   self.object_renderer = ObjectRenderer(self)
   self.ray_cast = RayCasting(self)
   self.object_handler = ObjectHandler(self)

  def update(self):
    self.player.update()
    self.ray_cast.update()
    self.object_handler.update()
    pg.display.flip()
    self.dt = self.clock.tick(FPS)
    pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

  def draw(self):
    # self.screen.fill('black')
    self.object_renderer.draw()
    # self.map.draw()
    # self.player.draw() # it's a moon now

  def check_event(self):
    keys = pg.key.get_pressed()
    for event in pg.event.get():
      if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()

  def run(self):
    while True:
      self.check_event()
      self.update()
      self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()