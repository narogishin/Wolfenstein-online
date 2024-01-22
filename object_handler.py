from sprite_object import AnimatedSprite, SpriteObject

class ObjectHandler:
  def __init__(self, game) -> None:
    self.game = game
    self.sprite_list = []
    self.static_sprite_path = 'ressources/sprites/static sprites'
    self.animated_sprite_path = 'ressources/sprites/animated sprites'
    add_sprite = self.add_sprite

    add_sprite(SpriteObject(game))
    add_sprite(AnimatedSprite(game))
    # for later customization, to add the wanted sprite images in the wanted positions

  def update(self):
    [sprite.update() for sprite in self.sprite_list]

  def add_sprite(self, sprite):
    self.sprite_list.append(sprite)