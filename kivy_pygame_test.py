'''
Created on Jan 16, 2017

@author: vivian

Something to test if it is possible to capture image data from a PyGame screen.

    - Starts with a base Kivy app.
    - Calls up a PyGame app with a window from within the Kivy app.
    - Assigns random colors to pixels in PyGame window.
    - Copies contents in PyGame window into a NumPy array.
    - Plots the NumPy array to see if it is the same as the PyGame window.
      (orientation is off, need to be rotated to get original window orientation)

Skeleton pygame app class PyGameApp adapted from:
    http://pygametutorials.wikidot.com/tutorials-basic
    
Requires:
    Python 3 (can run also in Python 2)
    kivy
    pygame
    matplotlib
    numpy
'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

#import pygame stuff
import pygame
from pygame.locals import *

import numpy as np
from matplotlib import pyplot as plt



#~ class PyGameApp(pb.Referenceable, Game.Game):
class PyGameApp:
    """Pygame main application"""
    
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
    
    def draw_random_screen(self):
        # assigns random color to each pixel on the screen
        self.screen = self._display_surf
        random_screen = np.random.randint(255, size=(self.width, self.height, 3))
        pygame.surfarray.blit_array(self.screen, random_screen)
        pygame.display.update()


class KivyMain(BoxLayout):        
    def __init__(self, **kwargs):
        super(KivyMain, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.pygame_app = PyGameApp()
        self.test_function()


    def test_function(self):
        self.pygame_app.draw_random_screen()
        data = self.screen_shot()
        plt.imshow(data, interpolation='nearest')
        plt.show()


    def screen_shot(self):
        # dumps contents on screen into a 3D array
        height = self.pygame_app.height
        width = self.pygame_app.width
        screenshot_3d_array = np.empty([width, height, 3], dtype=int)
        pygame.pixelcopy.surface_to_array(screenshot_3d_array, self.pygame_app.screen)
        return screenshot_3d_array


class KivyApp(App):
    def build(self):
        main_screen = KivyMain()
        return main_screen
    
    
def main():
    
    app = KivyApp()
    app.run()

    
if __name__ == "__main__":
    main()
