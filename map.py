import pygame 
from pytmx.util_pygame import load_pygame

class World:
    def __init__(self, path, screen):
        self.path = path
        self.data = load_pygame(path)
        self.ground = self.data.get_layer_by_name("layer")
        self.screen = screen
        
        for layer in self.data.visible_layers:
            setattr(self, layer.name, self.data.get_layer_by_name(layer.name))

        self.background = pygame.Surface((self.data.width*self.data.tilewidth, self.data.height*self.data.tileheight))
        
    def draw_background(self):
        for x,y, image in self.ground.tiles():
            self.background.blit(image,(x*self.data.tilewidth,y*self.data.tileheight))
        self.screen.blit(self.background,(0,0))