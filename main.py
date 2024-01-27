import pygame
import random
from graphics import *

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Graph Visualizer")

graph = Graph(6, screen)
graph.generateConnectedGraph()

algos = Algorithms(graph)

def draw_lines(edge, color):
    pygame.draw.line(screen, color, edge[0], edge[1], 2)

def draw_points(points):
    for point in points:
        pygame.draw.circle(screen, black, point, 5)


prims = (algos.primsAlgorithm())

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        graph.showGraph()
        algos.animateGraph(prims, graph.points)
        print("yeah")
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
