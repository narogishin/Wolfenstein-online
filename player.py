from settings import *
import pygame as pg
import math

class Player:
  def __init__(self, game) -> None:
    self.game = game
    self.x, self.y = PLAYER_POSITION
    self.angle = PLAYER_ANGLE

  def movement(self):
    sin_a = math.sin(self.angle)
    cos_a = math.cos(self.angle)
    dx, dy = 0, 0

    # if we want the player's mouvement speed to be independent to the frame rate then we need to get the delta time for each frame
    mvt = PLAYER_SPEED*self.game.dt
    mvt_sin = mvt*sin_a
    mvt_cos = mvt*cos_a

    keys = pg.key.get_pressed()
    if keys[pg.K_z]:
      dx += mvt_cos
      dy += mvt_sin
    if keys[pg.K_q]:
      dx += mvt_sin
      dy += -mvt_cos
    if keys[pg.K_s]:
      dx += -mvt_cos
      dy += -mvt_sin
    if keys[pg.K_d]:
      dx += -mvt_sin
      dy += mvt_cos

    self.x += dx
    self.y += dy

    if keys[pg.K_LEFT]:
      self.angle -= PLAYER_ROT_SPEED*self.game.dt
    if keys[pg.K_RIGHT]:
      self.angle += PLAYER_ROT_SPEED*self.game.dt

    self.angle %= 2*math.pi

  def draw(self):
    pg.draw.line(self.game.screen, 'yellow', (self.x*100, self.y*100),
                 (self.x*100 + WIDTH * math.cos(self.angle),
                  self.y*100 + WIDTH * math.sin(self.angle)), 2)
    pg.draw.circle(self.game.screen, 'green', (self.x*100, self.y*100), 15)

  def update(self):
    self.movement()

  @property
  def position(self):
    return self.x, self.y
  
  @property
  def map_position(self):
    return int(self.x), int(self.y)