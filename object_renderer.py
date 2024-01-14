import pygame as pg
from settings import *

class ObjectRenderer:
  def __init__(self, game) -> None:
    self.game = game
    self.screen = game.screen
    self.wall_textures = self.load_wall_textures()

  def draw(self):
    self.render_game_objects()

  def render_game_objects(self):
    list_objects = self.game.ray_cast.get_objects_to_render()
    for depth, image, position in list_objects:
      self.screen.blit(image, position)

  @staticmethod
  def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path).convert_alpha()
    return pg.transform.scale(texture, res)
  
  def load_wall_textures(self):
    return {i: self.get_texture(f"ressources/textures/wall tile {i}.png") 
            for i in range(1, 11)}