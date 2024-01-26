import random
import pygame
from time import sleep
from copy import deepcopy
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

def generate_random_points(num_points, screen_width, screen_height):
    points = []
    for _ in range(num_points):
        x = random.randint(50, screen_width - 50)
        y = random.randint(50, screen_height - 50)
        points.append((x, y))
    return points

class Graph:
    def __init__(self, num_points, screen):
        screen_width, screen_height = screen.get_size()
        self.num_points = num_points
        self.screen = screen
        self.points = generate_random_points(num_points, screen_width, screen_height)
        self.edges = set()
        self.edges2 = set()

    def distance(self,point1, point2):
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 )**0.5

    def generateConnectedGraph(self):
        connected_points = []
        unconnected_points = deepcopy(self.points)
        edges = set()
        edges2 = set()
        firstPoint = True
        secondPoint = True
        unconnected_points_len = deepcopy(self.num_points)
        while unconnected_points_len != 0:
            point = unconnected_points[random.randint(0, unconnected_points_len - 1)]
            unconnected_points_len -= 1
            unconnected_points.remove(point)
            if firstPoint:
                connected_points.append(point)
                firstPoint = False
                continue
            if (not firstPoint) and secondPoint:
                secondPoint = False
                index = 0
            else:
                index = random.randint(0, self.num_points - unconnected_points_len - 2)
            point_to_connect = connected_points[index]
            connected_points.append(point)
            dist = self.distance(point, point_to_connect)
            edges.add(tuple([point, point_to_connect, dist]))
            edges2.add(tuple([point, point_to_connect]))
        for i in range((self.num_points)//3):
            print(f"Goo{i}")
            point1 = connected_points[random.randint(0, self.num_points -1)]
            point2 = connected_points[random.randint(0, self.num_points -1)]

            print(f"the points first chosen are: {point1, point2}")
            while (point1 == point2) or (((point1, point2) in edges2) or ((point2, point1) in edges2)): 
                    point1 = connected_points[random.randint(0, self.num_points -1)]
                    point2 = connected_points[random.randint(0, self.num_points -1)]
            print(f"the points selected are: {point1, point2}")
            dist = self.distance(point1, point2)
            edges.add(tuple([point1, point2, dist]))
            edges2.add(tuple([point1, point2]))
        print(f"The current edges length {len(edges)}")
        print(edges)
        self.edges = edges
        self.edges2 = edges2

    def draw_lines(self, edge):
        pygame.draw.line(self.screen, red, edge[0], edge[1], 2)

    def draw_points(self):
        for point in self.points:
            pygame.draw.circle(self.screen, black, point, 5)

    def showGraph(self):
        self.screen.fill(white)
        self.draw_points()
        for edge in self.edges:
            self.draw_lines(edge)







