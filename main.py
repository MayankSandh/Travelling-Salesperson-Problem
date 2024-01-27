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

graph = Graph(10, screen)
# graph.generateConnectedGraph()
graph.generateCompleteGraph()
algos = Algorithms(graph)
otc = algos.oneTreeCost()




prims = (algos.primsAlgorithm())
NN = algos.NearestNeighbourHeuristic()
# prims_length = 

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # graph.showGraph()
        algos.showGraph(NN, graph.points)
        # algos.animateGraph(prims, graph.points)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
