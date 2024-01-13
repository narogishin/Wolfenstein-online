import os
import pygame as pg
from settings import *

class ObjectRenderer:
  def __init__(self, game) -> None:
    self.game = game
    self.screen = game.screen
    self.wall_textures = self.load_wall_textures()

  @staticmethod
  def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
    texture = pg.image.load(path).convert_alpha()
    return pg.transform.scale(texture, res)
  
  @staticmethod
  def count_files_in_folder(folder_path):
    file_count = sum(1 for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file)))
    return file_count
  
  def load_wall_textures(self):
    return {i: self.get_texture(f"resources/textures/wall tile {i}.png") 
            for i in range(1, 11)}