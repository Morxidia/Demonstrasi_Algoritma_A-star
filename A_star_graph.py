from scipy.spatial import KDTree
import heapq
import math
import time
import random
import numpy as np

class Graph:
    def __init__(self, graph, coordinate):
        self.vertex = graph
        self.coordinate = coordinate

    def heuristic(self, curr_vertex, target):
        x1, y1 = self.coordinate[curr_vertex]
        x2, y2 = self.coordinate[target]
        heuristic = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return heuristic

    def Astar_with_dijkstra(self, start, target):
        """
        start by initialize all the value to infinity on every vertex in graph
        initialize the target distance to 0
        predecessor for keep tracking of the sorthes paht in final graph
        """
        distance = {node: float("inf") for node in self.vertex}
        distance[start] = 0
        predecessor = {node: None for node in self.vertex}
        """
        declaring a heap data structure to keep tract of the smallest
        distance on the local graph to then finding the global optimal
        """
        priority_queue = [(0 + self.heuristic(start, target), 0, start)]
        heapq.heapify(priority_queue)
        visited = set()
        """
        doing the iteration on the heap until the heap was empty
        when heap is empty its guarented to fint the shortest distance
        """
        while len(priority_queue) != 0:
            h_value, curr_dist, curr_node = heapq.heappop(priority_queue)

            if curr_node == target:
                break
            if curr_node in visited:
                continue

            visited.add(curr_node)
            for neighbor, weight in self.vertex[curr_node].items():
                temp_distance = curr_dist + weight
                """
                check for the smallest distance from the old distance
                to the newest distance, and storing the smallest distance
                """
                if temp_distance < distance[neighbor]:
                    distance[neighbor] = temp_distance
                    predecessor[neighbor] = curr_node
                    """
                    calculate the final distance by adding the heuristic value
                    in the temp distance ensuring the heap will always storing
                    distance with heuristic value
                    """
                    final_distance = temp_distance + self.heuristic(neighbor, target)
                    heapq.heappush(
                        priority_queue, 
                        (final_distance,temp_distance, neighbor)
                    )

        return distance, predecessor, visited

    def djikstra(self, start, target):
        distance = {node: float("inf") for node in self.vertex}
        distance[start] = 0
        predecessor = {node: None for node in self.vertex}
        priority_queue = [(0, start)]
        heapq.heapify(priority_queue)
        visited = set()

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == target:
                break
            if current_node in visited:
                continue
            
            visited.add(current_node)
            for neighbor, weight in self.vertex[current_node].items():
                temp_distance = current_distance + weight
                if temp_distance < distance[neighbor]:
                    distance[neighbor] = temp_distance
                    predecessor[neighbor] = current_node
                    heapq.heappush(priority_queue, (temp_distance, neighbor))
        
        return distance, predecessor, visited

    def shortest_path(self, start, target, debug=False, algorithm="astar"):
        if start in self.vertex or target in self.vertex:
            time_start = time.perf_counter()
            if algorithm == "astar":
                distance, predecessor, visited = self.Astar_with_dijkstra(start, target)
            else:
                distance, predecessor, visited = self.djikstra(start, target)
            time_end = time.perf_counter()

            if debug:
                print(f"time excecution : {((time_end - time_start)* 1000):4f}ms")
            path = []
            curr_vertex = target
            while curr_vertex:
                path.append(curr_vertex)
                curr_vertex = predecessor[curr_vertex]
            path.reverse()
            return path, distance[target], visited
        return None

def calculate_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    actual_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    final_distance = weighted_random_connection() * actual_distance
    return round(final_distance)

def make_undirected_graph(graph):
    undirected_graph = {}
    for node in graph:
        undirected_graph[node] = graph[node].copy()

    # Add reverse connections
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            if neighbor not in undirected_graph:
                undirected_graph[neighbor] = {}
            undirected_graph[neighbor][node] = weight
            
    return undirected_graph

def create_limited_graph_optimized(positions, max_connections=3, min_connections=1):
    n = len(positions)
    nodes = list(positions.keys())
    
    # Precompute all distances
    edges = []
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes[i+1:], i+1):
            dist = calculate_distance(positions[node1], positions[node2])
            edges.append((dist, node1, node2))
    
    # Build Minimum Spanning Tree to ensure connectivity
    graph = kruskal_mst(nodes, edges)
    
    # Add random additional connections
    for node in nodes:
        local_max_connection = random.randint(min_connections, max_connections)
        current_connections = len(graph[node])
        
        if current_connections < local_max_connection:
            # Get potential new connections sorted by distance
            potential_connections = []
            for other in nodes:
                if other != node and other not in graph[node]:
                    dist = calculate_distance(positions[node], positions[other])
                    potential_connections.append((dist, other))
            
            potential_connections.sort()
            
            # Add random selection of new connections
            additional_needed = local_max_connection - current_connections
            # Randomly choose from top candidates (not just the closest)
            k = min(len(potential_connections), additional_needed * 2)
            if k > 0:
                selected = random.sample(potential_connections[:k], 
                                       min(additional_needed, k))
                for dist, neighbor in selected:
                    graph[node][neighbor] = dist
                    graph[neighbor][node] = dist
    
    return graph

def kruskal_mst(nodes, edges):
    """Kruskal's algorithm for Minimum Spanning Tree"""
    edges.sort()
    parent = {node: node for node in nodes}
    graph = {node: {} for node in nodes}
    
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]
    
    def union(node1, node2):
        root1, root2 = find(node1), find(node2)
        if root1 != root2:
            parent[root2] = root1
            return True
        return False
    
    for dist, node1, node2 in edges:
        if union(node1, node2):
            graph[node1][node2] = dist
            graph[node2][node1] = dist
    
    return graph

def weighted_random_connection():
    # Probabilities: 2-3=50%, 1-2=35%, 2-5=15%
    rand_val = random.random()
    if rand_val < 0.5:
        return random.uniform(2, 3)
    elif rand_val < 0.85: 
        return random.uniform(1, 2)
    else:
        return random.uniform(3, 5)


def create_random_pos(num_pos=10, default_pos=None, default_x=500, default_y = 500):
    coordinate = {}
    max_x = 0
    min_y = 0
    if default_pos is not None:
        coordinate.update(default_pos)
        max_x = max(x for x,y in default_pos.values()) * 2
        min_y = max(y for x,y in default_pos.values()) * -1
    alphabets = [chr(ord("A") + i) for i in range(26)]
    index = 0

    max_num = math.ceil(num_pos/26)
    while len(coordinate) <= num_pos:
        for i in range(max_num):
            key = str(alphabets[index]) + str(i + 1)
            coordinate[key] = (
                random.randint(0, max_x),
                random.randint(min_y, 850),
            )
            if len(coordinate) > num_pos:
                break
        index+=1
    
    return coordinate
