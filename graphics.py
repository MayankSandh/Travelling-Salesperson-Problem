import random
import pygame
from copy import deepcopy
import numpy as np

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

    def generateCompleteGraph(self):
        edges = set()
        edges2 = set()
        points = self.points
        for i in range(len(points)-1):
            for j in range(i+1, len(points)):
                edges.add(tuple([points[i], points[j], self.distance(points[i], points[j])]))
                edges2.add(tuple([points[i], points[j]]))
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

    def __init__(self, graph: Graph, screen):
        self.graph = graph
        self.MST_len = self.calculateMSTLength(self.graph.edges, self.graph.points)
        self.screen = screen
        self.OTC = self.oneTreeCost()

    def calculatePathLength(self, edges):
        return sum([edge[2] for edge in edges])
    
    def CycleDetected(self, edges, points, check_edge): # isolated edges should be coloured first
        detector = dict()
        for point in points:
            detector[point] = False
        point0, point1 = check_edge[0], check_edge[1]
        detector[point0] = False
        detector[point1] = False
        for edge in edges:
            point0, point1 = edge[0], edge[1]
            if (detector[point0] and detector[point1]):
                return True
            else:
                if detector[point0] == True:
                    detector[point1] = True
                elif detector[point1] == True:
                    detector[point0] = True
        point0, point1 = check_edge[0], check_edge[1]
        if (detector[point0] and detector[point1]):
            return True
        return False

    def NearestNeighbourHeuristic(self):
        edges = []
        startingPoint = self.graph.points[random.randint(0, self.graph.num_points - 1)]
        connected_edges = dict()
        for point in self.graph.points:
            connected_edges[point] = []
        i = 0
        myedges = list(self.graph.edges)
        for edge in myedges:
            connected_edges[edge[0]].append(i)
            connected_edges[edge[1]].append(i)
            i+=1
        currPoint = deepcopy(startingPoint)
        visitedCities = set()
        visitedCities.add(currPoint)
        for k in range(self.graph.num_points-1):
            curr_edges = sorted([myedges[i] for i in connected_edges[currPoint]], key=lambda x: x[2])
            for edge in curr_edges:
                if edge[0] == currPoint:
                    point_connected = edge[1]
                else:
                    point_connected = edge[0]
                if point_connected not in visitedCities:
                    currPoint = point_connected
                    visitedCities.add(currPoint)
                    edges.append(edge)
                    break

        for edge_index in connected_edges[startingPoint]:
            edge = myedges[edge_index]
            if edge[0] == startingPoint:
                point_connected = edge[1]
            else:
                point_connected = edge[0]
            if point_connected == currPoint:
                edges.append(edge)
        print(f"MST-Ratio:- {self.calculatePathLength(edges)/self.MST_len}")
        return edges

    def primsAlgorithm(self):
        MST = []
        connected_edges = dict()
        for point in self.graph.points:
            connected_edges[point] = []
        i = 0
        myedges = list(self.graph.edges)
        for edge in myedges:
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

    def calculateMSTLength(self, edges, points):
        MST_len = 0
        connected_edges = dict()
        for point in points:
            connected_edges[point] = []
        i = 0
        myedges = list(edges)
        for edge in myedges:
            connected_edges[edge[0]].append(i)
            connected_edges[edge[1]].append(i)
            i+=1
        MST_points = set()
        non_MST_points = deepcopy(points)
        first = True
        non_MST_points_len = deepcopy(len(point))
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

            MST_len+=min_path_edge[2]
            if min_path_edge[0] in MST_points:
                point2 = min_path_edge[1]
            else:
                point2 = min_path_edge[0]
            MST_points.add(point2)
            non_MST_points.remove(point2)
        return MST_len    

    def draw_lines(self, edge, color, width):
        pygame.draw.line(self.graph.screen, color, edge[0], edge[1], width)

    def draw_points(self, points):
        for point in points:
            pygame.draw.circle(self.graph.screen, black, point, 5)

    def animateGraph(self, edges, points):
        self.graph.screen.fill(white)
        for edge in self.graph.edges:
            self.draw_lines(edge, (255, 127, 127), 4)
        self.draw_points(points)
        for edge in edges:
            self.draw_lines(edge, (138,43,226), 6)
            pygame.display.flip()
            pygame.time.delay(400)
    
    def showGraph(self, edges, points):
        self.graph.screen.fill(white)
        for edge in self.graph.edges:
            self.draw_lines(edge, (255, 127, 127), 4)
        self.draw_points(points)
        for edge in edges:
            self.draw_lines(edge, (138,43,226), 6)

    def oneTreeCost(self):
        connected_edges = dict()
        top_two_edges = dict()
        for point in self.graph.points:
            connected_edges[point] = []
            top_two_edges[point] = 0.0
        i = 0
        myedges = list(self.graph.edges)
        for edge in myedges:
            connected_edges[edge[0]].append(i)
            connected_edges[edge[1]].append(i)
            i+=1
        for point in self.graph.points:
            min = 1000000
            min_2nd = 1000000
            for edge in connected_edges[point]:
                if myedges[edge][2] < min:
                    min = myedges[edge][2]
                elif myedges[edge][2] < min_2nd:
                    min_2nd = myedges[edge][2]
            top_two_edges[point] = min+min_2nd
        max_t_cost = 0
        for point in self.graph.points:
            new_points = deepcopy(self.graph.points)
            new_points.remove(point)
            new_edges = deepcopy(myedges)
            edges_to_be_removed = [myedges[i] for i in connected_edges[point]]
            for edge_r in edges_to_be_removed:
                new_edges.remove(edge_r)
            val = self.calculateMSTLength(new_edges, new_points) + top_two_edges[point]
            if max_t_cost < val:
                max_t_cost = val 
        return max_t_cost

    def antColonyOptimisation(self, screen, iterations = 10000):
        for edge in self.graph.edges:
            self.draw_lines(edge, (255, 127, 127), 4)
        self.draw_points(self.graph.points)
        rewardMatrix = np.ones(shape=(self.graph.num_points, self.graph.num_points))
        for i in range(1, iterations+1):
            print(f"~~~~~~~~~~~~~~~~~ITERATION-{i}~~~~~~~~~~~~~~~~~~")
            self.graph.screen.fill(white)
            for edge in self.graph.edges:
                self.draw_lines(edge, (255, 127, 127), 4)
            self.draw_points(self.graph.points)
            edges = []
            startingPoint = self.graph.points[random.randint(0, self.graph.num_points - 1)]
            connected_edges = dict()
            for point in self.graph.points:
                connected_edges[point] = []
            i = 0
            myedges = list(self.graph.edges)
            for edge in myedges:
                connected_edges[edge[0]].append(i)
                connected_edges[edge[1]].append(i)
                i+=1
            currPoint = deepcopy(startingPoint)
            visitedCities = set()
            visitedCities.add(currPoint)
            for k in range(self.graph.num_points - 1):
                curr_edges = [myedges[i] for i in connected_edges[currPoint]]
                allowed_edges = []
                for edge in curr_edges:
                    if edge[0] == currPoint:
                        point_connected = edge[1]
                    else:
                        point_connected = edge[0]
                    if point_connected not in visitedCities:
                        allowed_edges.append(edge)
                weights = np.reciprocal(np.array([i[2]/rewardMatrix[self.graph.points.index(i[0])][self.graph.points.index(i[1])] for i in allowed_edges]))
                weights = weights/np.sum(weights)
                chosen_edge = allowed_edges[np.random.choice(np.arange(len(weights)),  p=weights)]
                if chosen_edge[0] == currPoint:
                    currPoint = chosen_edge[1]
                else:
                    currPoint = chosen_edge[0]
                edges.append(chosen_edge)
                self.draw_lines(chosen_edge, (138,43,226), 6)
                pygame.display.flip()
                pygame.time.delay(100)
                visitedCities.add(currPoint)
            for edge_index in connected_edges[startingPoint]:
                edge = myedges[edge_index]
                if edge[0] == startingPoint:
                    point_connected = edge[1]
                else:
                    point_connected = edge[0]
                if point_connected == currPoint:
                    edges.append(edge)
                pygame.display.flip()
                pygame.time.delay(100)
            score = self.calculatePathLength(edges)
            for edge in edges:
                point0, point1 = edge[0], edge[1]
                row = self.graph.points.index(point0)
                col = self.graph.points.index(point1)
                rewardMatrix[row][col] += 1/score
                rewardMatrix[col][row] += 1/score
            print(f"OTC-Ratio:- {self.calculatePathLength(edges)/self.OTC}")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
