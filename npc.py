from sprite_object import SpriteObject, AnimatedSprite
from random import randint, random, choice
from settings import *
import pygame as pg

class NPC(AnimatedSprite):
  def __init__(self, game, path='ressources/sprites/npc/soldier/0.png', pos=(10.5, 5.5), scale=0.6, shift=0.36,
                animation_time=120):
    super().__init__(game, path, pos, scale, shift, animation_time)
    self.attack_images = self.get_images(self.path + '/attack')
    self.death_images = self.get_images(self.path + '/death')
    self.idle_images = self.get_images(self.path + '/idle')
    self.pain_images = self.get_images(self.path + '/pain')
    self.walk_images = self.get_images(self.path + '/walk')

    self.attack_dist = randint(3, 6)
    self.speed = 0.03
    self.size = 10
    self.health = 100
    self.attack_damage = 10
    self.accuracy = 0.15
    self.alive = True
    self.pain = False
    self.frame_counter = 0

  def update(self):
    self.check_animation_time()
    self.get_sprite()
    self.run_logic()
    # self.draw_ray_cast()

  def animate_pain(self):
    self.animate(self.pain_images)
    self.game.sound.player_pain.play()
    if self.animation_trigger:
      self.pain = False

  def animate_death(self):
      if not self.alive:
        if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
          self.death_images.rotate(-1)
          self.image = self.death_images[0]
          self.frame_counter += 1
          # we could add here somthing to stop the player's mouvement because he is dead
          # self.game.object_handler.npcs.pop(self.game.player.name) 

  def check_hit_in_npc(self):
    if self.game.player.shot and self.ray_cast_value and HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
      # making sure that the sprite is aligned with the gun and the player had pressed the button to kill npc
      self.pain = True
      # should it be here ? or just use another player.variable like shoot and make it the same state as this self.pain ?
      self.game.player.shot = False
      # why setting it here to false ? maybe we should wait for next animation to make sure the old animation is played
      self.health -= self.game.weapon.damage
      self.check_health()

  def check_health(self):
    if self.health <= 0:
      self.alive = False
      self.game.sound.npc_death.play()
    
  def run_logic(self):
    # old_x, old_y = int(self.x), int(self.y)
    if self.alive:
      self.ray_cast_value = self.ray_cast_player_npc()
      self.check_hit_in_npc()
      if self.pain:
        self.animate_pain()
      else:
        self.animate(self.idle_images)
      # if (old_x, old_y) != self.map_pos:
      #   self.animate(self.walk_images)
    else:
      self.animate_death()

  @property
  def map_pos(self):
    return int(self.x), int(self.y)
  
  def horizontal_ray_cast(self, sin_a, cos_a, ox, oy, y_map):
      wall_dist_h, player_dist_h = 0, 0
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
        if tile_hor == self.map_pos:
          player_dist_h = depth_hor
          break
        if tile_hor in self.game.map.world_map:
          wall_dist_h = depth_hor
          break
        else:
          x_hor += dx
          y_hor += dy
          depth_hor += delta_depth
      return player_dist_h, wall_dist_h

  def vertical_ray_cast(self, sin_a, cos_a, ox, oy, x_map):
      wall_dist_v, player_dist_v = 0, 0
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
          wall_dist_v = depth_vert
          break
        if tile_vert == self.map_pos:
          player_dist_v = depth_vert
          break
        else:
          x_vert += dx
          y_vert += dy
          depth_vert += delta_depth
      return player_dist_v, wall_dist_v

  def ray_cast_player_npc(self):
    # checking if the player is in the same tile as the NPC
    if self.game.player.map_position == self.map_pos:
      return True
    
    ox, oy = self.game.player.position
    x_map, y_map = self.game.player.map_position
    ray_angle = self.theta

    cos_a = math.cos(ray_angle)
    sin_a = math.sin(ray_angle)

    # do understand what is the offset, one should know what it's used for
    # and why the case of sin is the inverse of the case of cos ?
    player_dist_h, wall_dist_h = self.horizontal_ray_cast(sin_a, cos_a, ox, oy, y_map)
    player_dist_v, wall_dist_v = self.vertical_ray_cast(sin_a, cos_a, ox, oy, x_map)

    player_dist = max(player_dist_v, player_dist_h)
    wall_dist = max(wall_dist_v, wall_dist_h)

    if 0 < player_dist < wall_dist or not wall_dist:
      return True
    
    return False
  
  def draw_ray_cast(self):
    pg.draw.circle(self.game.screen, 'red', (100*self.x, 100*self.y), 15)
    if self.ray_cast_player_npc():
      pg.draw.line(self.game.screen, 'orange', (100*self.game.player.x, 100*self.game.player.y), (100*self.x, 100*self.y), 2)