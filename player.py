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

    # if we want the player's mouvement speed to be independent 
    # from the frame rate then we need to get the delta time for each frame
    # hence the "dt" term from clock tick
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

    self.check_wall_collision(dx, dy)

    # disabled for we are using mouse right now
    # if keys[pg.K_LEFT]:
    #   self.angle -= PLAYER_ROT_SPEED*self.game.dt
    # if keys[pg.K_RIGHT]:
    #   self.angle += PLAYER_ROT_SPEED*self.game.dt

    self.angle %= 2*math.pi

  def check_wall(self, x, y):
    return (x, y) not in self.game.map.world_map
  
  def check_wall_collision(self, dx, dy):
    scale = PLAYER_SIZE_SCALE / self.game.dt
    if self.check_wall(int(self.x+dx*scale), int(self.y)):
      self.x += dx
    if self.check_wall(int(self.x), int(self.y+dy*scale)):
      self.y += dy

  def draw(self):
    pg.draw.line(self.game.screen, 'yellow', (self.x*100, self.y*100),
                 (self.x*100 + WIDTH * math.cos(self.angle),
                  self.y*100 + WIDTH * math.sin(self.angle)), 2)
    pg.draw.circle(self.game.screen, 'green', (self.x*100, self.y*100), 15)

  def mouse_control(self):
    mx, my = pg.mouse.get_pos()
    if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
      # I think I got what this is saying, it's like it borders
      # the mouse mvts to h & w of screen, and it strats
      # counting from the center is that right ? i'm just guessing,
      # I'll look for it later, should add this the my action list
      pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
      # idk what it is, feeling tired after work, I can look for 
      # meaning of these methods tomorrow or when I'm not 
      # waking up early next morning.
    self.rel = pg.mouse.get_rel()[0]
    self.rel = max(-MOUSE_MAX_RELATIVE_MOUVEMENT, 
                   min(MOUSE_MAX_RELATIVE_MOUVEMENT, self.rel))
    self.angle += self.rel * MOUSE_SENSITIVITY * self.game.dt

  def update(self):
    self.movement()
    self.mouse_control()

  @property
  def position(self):
    return self.x, self.y
  
  @property
  def map_position(self):
    return int(self.x), int(self.y)