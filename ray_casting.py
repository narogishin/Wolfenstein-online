import pygame as pg
from settings import *
import math

class RayCasting:
  def __init__(self, game) -> None:
    self.game = game
    self.ray_casting_result = []
    self.objects_to_render = []
    self.textures = self.game.object_renderer.wall_textures

  def get_objects_to_render(self):
    self.objects_to_render = []
    for ray, values in enumerate(self.ray_casting_result):
      depth, projected_height, texture, offset = values

      wall_column = self.textures[texture].subsurface(
        offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
      )
      wall_column = pg.transform.scale(wall_column, (SCALE, projected_height))
      wall_position = (ray * SCALE, HALF_HEIGHT - projected_height // 2)

      self.objects_to_render.append((depth, wall_column, wall_position))

    return self.objects_to_render

  def horizontal_ray_cast(self, sin_a, cos_a, ox, oy, y_map):
      texture_hor = 1
      # still need to know about that -1e-6 
      y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
      # my answer : it's used to round x_map to it's previous value, if not it'll it's actual value
      depth_hor = (y_hor - oy) / sin_a
      x_hor = ox + depth_hor * cos_a

      delta_depth = dy / sin_a
      dx = delta_depth * cos_a

      for i in range(MAX_DEPTH):
        tile_hor = int(x_hor), int(y_hor)
        if tile_hor in self.game.map.world_map:
          texture_hor = self.game.map.world_map[tile_hor]
          break
        else:
          x_hor += dx
          y_hor += dy
          depth_hor += delta_depth
      return depth_hor, texture_hor, y_hor, x_hor

  def vertical_ray_cast(self, sin_a, cos_a, ox, oy, x_map):
      texture_vert = 1
      # still need to know about that -1e-6 
      x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
      # my answer : it's used to round x_map to it's previous value, if not it'll it's actual value
      
      depth_vert = (x_vert - ox) / cos_a
      y_vert = oy + depth_vert * sin_a

      # dy = dx*math.tan(ray_angle)
      delta_depth = dx / cos_a
      dy = delta_depth * sin_a

      for i in range(MAX_DEPTH):
        tile_vert = int(x_vert), int(y_vert)
        if tile_vert in self.game.map.world_map:
          texture_vert = self.game.map.world_map[tile_vert]
          break
        else:
          x_vert += dx
          y_vert += dy
          depth_vert += delta_depth
      return depth_vert, texture_vert, y_vert, x_vert

  def ray_cast(self):
    ox, oy = self.game.player.position
    x_map, y_map = self.game.player.map_position
    ray_angle = self.game.player.angle - HALF_FOV + 0.0001 # added to avoid division by zero
    self.ray_casting_result = []

    for ray in range(NUM_RAYS):
      cos_a = math.cos(ray_angle)
      sin_a = math.sin(ray_angle)

      depth_hor, texture_hor, y_hor, x_hor = self.horizontal_ray_cast(sin_a, cos_a, ox, oy, y_map)
      depth_vert, texture_vert, y_vert, x_vert = self.vertical_ray_cast(sin_a, cos_a, ox, oy, x_map)

      if depth_vert < depth_hor:
        depth, texture = depth_vert, texture_vert
        y_vert %= 1
        offset = y_vert if cos_a > 0 else (1 - y_vert)
      else:
        depth, texture = depth_hor, texture_hor
        x_hor %= 1
        offset = (1 - x_hor) if sin_a > 0 else x_hor
      
      projected_height = 1 * SCREEN_DISTANCE / (depth * math.cos(self.game.player.angle - ray_angle) + 0.0001)

      # pg.draw.line(self.game.screen, 'yellow', (ox*100, oy*100), 
      #              (100*ox + 100*depth*cos_a, 100*oy + 100*depth*sin_a), 2)

      color = [255/(1+ depth ** 5 * 0.00001)]*3

      # pg.draw.rect(self.game.screen, color, (ray * SCALE, HALF_HEIGHT - projected_height // 2, SCALE, projected_height))

      # ray casting results
      self.ray_casting_result.append((depth, projected_height, texture, offset))

      ray_angle+=DELTA_ANGLE

  def update(self):
    self.ray_cast()
    self.get_objects_to_render()