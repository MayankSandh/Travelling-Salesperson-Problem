import pygame
import random
from graphics import *

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Graph Visualizer")

graph = Graph(20, screen)
graph.generateConnectedGraph()


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        graph.showGraph()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
