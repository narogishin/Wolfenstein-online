from sprite_object import SpriteObject, AnimatedSprite
from random import randint, random, choice
from settings import *

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

  def update(self):
    self.check_animation_time()
    self.get_sprite()
    self.run_logic()

  def animate_pain(self):
    self.animate(self.pain_images)
    self.game.sound.player_pain.play()
    if self.animation_trigger:
      self.pain = False

  def check_hit_in_npc(self):
    if self.game.player.shot and HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
      # making sure that the sprite is aligned with the gun and the player had pressed the button to kill npc
      self.pain = True
      # should it be here ? or just use another player.variable like shoot and make it the same state as this self.pain ?
      self.game.player.shot = False
      # why setting it here to false ? maybe we should wait for next animation to make sure the old animation is played
    
  def run_logic(self):
    if self.alive:
      self.check_hit_in_npc()
      if self.pain:
        self.animate_pain()
      else:
        self.animate(self.walk_images)