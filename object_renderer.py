import pygame as pg
from settings import *

class ObjectRenderer:
  def __init__(self, game) -> None:
    self.game = game
    self.screen = game.screen
    self.wall_textures = self.load_wall_textures()
    self.sky_image = self.get_texture("resources/textures/sky.png", (WIDTH, HALF_HEIGHT))
    self.sky_offset = 0

  def draw(self):
    self.draw_backgroud()
    self.render_game_objects()

  def draw_backgroud(self):
    # what does it have to do with rel ?
    self.sky_offset = (self.sky_offset + 4 * self.game.player.rel) % WIDTH
    self.screen.blit(self.sky_image, (-self.sky_offset, 0))
    self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

    # drawing the floor
    # pg.draw.rect(self.game.screen, (120,0,100), (0, 0, WIDTH, HEIGHT)
    pg.draw.rect(self.game.screen, (30,30,30), (0, HALF_HEIGHT, WIDTH, HEIGHT))

  def render_game_objects(self):
    list_objects = sorted(self.game.ray_cast.objects_to_render, key=lambda t: t[0], reverse=True)
    for depth, image, position in list_objects:
      self.screen.blit(image, position)

  @staticmethod
  def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path).convert_alpha()
    return pg.transform.scale(texture, res)
  
  def load_wall_textures(self):
    return {i: self.get_texture(f"resources/textures/wall tile {i}.png") 
            for i in range(1, 11)}