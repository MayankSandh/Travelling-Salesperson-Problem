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
            point1 = connected_points[random.randint(0, self.num_points -1)]
            point2 = connected_points[random.randint(0, self.num_points -1)]
            while (point1 == point2) or (((point1, point2) in edges2) or ((point2, point1) in edges2)): 
                    point1 = connected_points[random.randint(0, self.num_points -1)]
                    point2 = connected_points[random.randint(0, self.num_points -1)]
            dist = self.distance(point1, point2)
            edges.add(tuple([point1, point2, dist]))
            edges2.add(tuple([point1, point2]))
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

class Algorithms:

    def __init__(self, graph: Graph):
        self.graph = graph
    
    def primsAlgorithm(self):
        MST = []
        connected_edges = dict()
        for point in self.graph.points:
            connected_edges[point] = []
        i = 0
        myedges = list(self.graph.edges)
        for edge in self.graph.edges:
            connected_edges[edge[0]].append(i)
            connected_edges[edge[1]].append(i)
            i+=1
        MST_points = set()
        non_MST_points = deepcopy(self.graph.points)
        first = True
        non_MST_points_len = deepcopy(self.graph.num_points)
        point = non_MST_points[random.randint(0, non_MST_points_len - 1)]
        while non_MST_points:
            if first:
                non_MST_points.remove(point)
                MST_points.add(point)
                first = False
                continue

            min_path_len = 1000000
            min_path = -1
            for point in MST_points:
                for path_edge_index in connected_edges[point]:
                    path_edge = myedges[path_edge_index]
                    if path_edge[0] == point:
                        point2 = path_edge[1]
                    else:
                        point2 = path_edge[0]
                    if point2 in MST_points:
                        continue
                    if path_edge[2] < min_path_len:
                        min_path_len = path_edge[2]
                        min_path = path_edge_index
            min_path_edge = myedges[min_path]

            MST.append(min_path_edge)
            if min_path_edge[0] in MST_points:
                point2 = min_path_edge[1]
            else:
                point2 = min_path_edge[0]
            MST_points.add(point2)
            non_MST_points.remove(point2)
        return MST
            
    def draw_lines(self, edge, color):
        pygame.draw.line(self.graph.screen, color, edge[0], edge[1], 4)

    def draw_points(self, points):
        for point in points:
            pygame.draw.circle(self.graph.screen, black, point, 5)

    def animateGraph(self, edges, points):
        for edge in self.graph.edges:
            self.draw_lines(edge, (255, 127, 127))
        self.draw_points(points)
        for edge in edges:
            self.draw_lines(edge, (138,43,226))
            pygame.display.flip()
            pygame.time.delay(100)
            
    # def animate_lines(self, edges, points):
    #     self.draw_points(points)
    #     for i in range(len(edges)-1):
    #         start_point = edges[i][0]
    #         end_point = edges[i+1][1]
    #         for j in range(1, 51):  # Number of steps for animation
    #             fraction = j / 50.0
    #             x = int(start_point[0] + fraction * (end_point[0] - start_point[0]))
    #             y = int(start_point[1] + fraction * (end_point[1] - start_point[1]))
    #             pygame.draw.circle(self.graph.screen, red, (x, y), 2)
    #             pygame.display.flip()
    #             pygame.time.delay(10)  # Delay between each step








