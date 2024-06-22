import pygame as pg
import sys
from settings import RESOLUTION, FPS
from map import Map
from client import Client
from player import Player
from ray_casting import RayCasting
from object_handler import ObjectHandler
from object_renderer import ObjectRenderer
from sprite_object import SpriteObject
from sound import Sound
from weapon import Weapon

class Game:
  def __init__(self) -> None:
    pg.init()
    pg.mouse.set_visible(False)
    self.screen = pg.display.set_mode(RESOLUTION)
    self.clock = pg.time.Clock()
    # what's the meaning of the following 3 lines ?
    self.global_trigger = False
    self.global_event = pg.USEREVENT + 0
    pg.time.set_timer(self.global_event, 40)
    self.dt = 1
    self.new_game()

  def new_game(self):
   self.map = Map(self)
   self.player = Player(self)
   self.object_renderer = ObjectRenderer(self)
   self.sprite_object = SpriteObject(self)
   self.ray_cast = RayCasting(self)
   self.object_handler = ObjectHandler(self)
   self.weapon = Weapon(self)
   self.client = Client(self)
   self.sound = Sound()

  def update(self):
    self.player.update()
    self.ray_cast.update()
    self.object_handler.update()
    self.weapon.update()
    pg.display.flip()
    self.client.update()
    self.dt = self.clock.tick(FPS)
    pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

  def draw(self):
    self.screen.fill('black')
    self.object_renderer.draw()
    self.weapon.draw()
    self.client.draw()
    # self.map.draw()
    # self.player.draw() # it's a moon now

  def check_event(self):
    self.global_trigger = False
    keys = pg.key.get_pressed()
    for event in pg.event.get():
      if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
        self.client.disconnect()
        pg.quit()
        sys.exit()
      elif event.type == self.global_event:
        self.global_trigger = True
      self.player.single_fire_event(event)

  def run(self):
    while True:
      self.check_event()
      self.update()
      self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()