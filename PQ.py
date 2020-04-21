from heapq import heappush, heappop, heapify
import itertools
import sys


class Vertex:
    def __init__(self, i, j, index):
        self.index = index
        self.i = i
        self.j = j
        self.distance = sys.maxsize
        self.predecessor = None
        self.adjacent = []
        self.visited = False
        self.pixel_type = 'normal'

    def set_distance(self, distance):
        self.distance = distance

    def get_predecessor(self):
        return self.predecessor

    def get_distance(self):
        return self.distance

    def set_pixel_type(self, pixel_type):
        self.pixel_type = pixel_type

    def set_visited(self):
        self.visited = True

    def get_pixel_type(self):
        return self.pixel_type

    def set_predecessor(self, predecessor):
        self.predecessor = predecessor

    def add_neighbour(self, neighbour):
        self.adjacent.append(neighbour)

    def get_neighbours(self):
        return self.adjacent

    def get_index(self):
        return self.index

    def get_i(self):
        return self.i

    def get_neighbours_index(self, width, height):
        i = self.get_i()
        j = self.get_j()
        neighbours = []

        if i >= 0 and j - 1 >= 0:
            neighbours.append((i, j - 1))

        if i >= 0 and j + 1 <= height:
            neighbours.append((i, j + 1))

        if i - 1 >= 0 and j >= 0:
            neighbours.append((i - 1, j))

        if i + 1 <= width and j >= 0:
            neighbours.append((i + 1, j))

        return neighbours

    def get_j(self):
        return self.j


class Graph:
    def __init__(self):
        self.node_count = 0
        self.vertices = {}

    def add_vertex_by_index(self, i, j, index):
        self.node_count += 1
        vertex = Vertex(i, j, index)
        self.vertices[index] = vertex
        return vertex

    def add_vertex_by_obj(self, vertex):
        self.node_count += 1
        self.vertices[vertex.get_index()] = vertex
        return vertex

    def get_vertex(self, index):
        if index in self.vertices:
            return self.vertices[index]
        else:
            return None

    def get_vertices(self):
        return self.vertices


def shortest(vertex, path):
    if vertex.get_predecessor():
        path.append(vertex.get_predecessor())
        shortest(vertex.get_predecessor(), path)
    return


def get_weight(v1, v2):
    if v1.get_pixel_type() == 'wall' or v2.get_pixel_type() == 'wall':
        return sys.maxsize

    else:
        return 1


def add_vertex(vertex, pq, entry_finder, counter):
    if vertex.get_index() in entry_finder:
        remove_vertex(vertex, entry_finder)
    count = next(counter)
    entry = (vertex.get_distance(), count, vertex)
    entry_finder[vertex.get_index()] = entry
    heappush(pq, entry)


def remove_vertex(v, entry_finder):
    entry = entry_finder.pop(v.get_index())


def pop_vertex(pq, entry_finder):
    while pq:
        priority, count, vertex = heappop(pq)
        if vertex:
            if vertex.get_index() in entry_finder:
                del entry_finder[vertex.get_index()]
                return vertex
    raise KeyError('pop from an empty priority queue')


# this function is not used in grid.py because animations needed to be added, but it works by itself as well
def dijkstra(current_graph, start):
    start.set_distance(0)
    pq = []
    entry_finder = {}
    counter = itertools.count()

    for value in current_graph.get_vertices().values():
        add_vertex(value, pq, entry_finder, counter)

    while len(pq):
        current_v = pop_vertex(pq, entry_finder)
        if current_v == None:
            break
        if current_v.visited or current_v.get_pixel_type() == 'wall':
            continue
        current_v.set_visited()

        # check neighbour nodes of the current vertex
        neighbours = current_v.get_neighbours()
        for neighbour in neighbours:
            weight = get_weight(current_v, neighbour)

            if current_v.get_distance() + weight < neighbour.get_distance():
                neighbour_in_graph = current_graph.get_vertex(neighbour.get_index())
                neighbour_in_graph.set_distance(current_v.get_distance() + weight)
                neighbour_in_graph.set_predecessor(current_v)

                # add entry to priority queue
                add_vertex(neighbour_in_graph, pq, entry_finder, counter)

                neighbour.set_distance(current_v.get_distance() + weight)
                neighbour.set_predecessor(current_v)
