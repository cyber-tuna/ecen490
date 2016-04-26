from collections import defaultdict, deque
import sys

rows = 5
cols = 5

points = [[0 for x in range(2*rows)] for x in range(2*cols)]

for row in range((-rows+1), rows):
        for col in range((-cols+1), cols):
            points[row][col] = str(row) + ',' + str(col)

impediments = list()


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def set_impediment(self, row, col):

        impediments.append(points[row][col])

        current_node = points[row][col]

        row_bound = rows - 1
        col_bound = cols - 1

        # west edge
        if col > 0:
            self.set_edge_distance(current_node, points[row][col-1], 999)

        # north-west edge
        if col > 0 and row > 0:
            self.set_edge_distance(current_node, points[row-1][col-1], 999)

        # north edge
        if row > 0:
            self.set_edge_distance(current_node, points[row-1][col], 999)

        # north-east edge
        if row > 0 and col < col_bound:
            self.set_edge_distance(current_node, points[row-1][col+1], 999)

        # east edge
        if col < col_bound:
            self.set_edge_distance(current_node, points[row][col+1], 999)

        # south-east edge
        if row < row_bound and col < col_bound:
            self.set_edge_distance(current_node, points[row+1][col+1], 999)

        # south edge
        if row < row_bound:
            self.set_edge_distance(current_node, points[row+1][col], 999)

        # south-west edge
        if row < row_bound and col > 0:
            self.set_edge_distance(current_node, points[row+1][col-1], 999)


    def set_edge_distance(self,from_node, to_node, distance):
        self.distances[(from_node, to_node)] = distance

    def print_distances(self):
        print self.distances

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


def dijkstra(graph, initial):
    print "start dijkstra"
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    print "end dijkstra"
    return visited, path


def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)


def create_graph():
    graph = Graph()

    row_bound = rows - 1
    col_bound = cols - 1

    for row in range((-rows+1), rows):
        for col in range((-cols+1), cols):
            graph.add_node(points[row][col])

            current_node = points[row][col]

            # west edge
            if col > 0:
                graph.add_edge(current_node, points[row][col-1], 1)

            # north-west edge
            if col > 0 and row > 0:
                graph.add_edge(current_node, points[row-1][col-1], 1.5)

            # north edge
            if row > 0:
                graph.add_edge(current_node, points[row-1][col], 1)

            # north-east edge
            if row > 0 and col < col_bound:
                graph.add_edge(current_node, points[row-1][col+1], 1.5)

            # east edge
            if col < col_bound:
                graph.add_edge(current_node, points[row][col+1], 1)

            # south-east edge
            if row < row_bound and col < col_bound:
                graph.add_edge(current_node, points[row+1][col+1], 1.5)

            # south edge
            if row < row_bound:
                graph.add_edge(current_node, points[row+1][col], 1)

            # south-west edge
            if row < row_bound and col > 0:
                graph.add_edge(current_node, points[row+1][col-1], 1.5)

    return graph

def print_path(path):
    for row in range((-rows+1), rows):
        for col in range((-cols+1), cols):
            if points[row][col] in path:
                sys.stdout.write(' . ')
            elif points[row][col] in impediments:
                sys.stdout.write("[@]")
            else:
                sys.stdout.write('(' + points[row][col] +")" + " ")
                #sys.stdout.write(' O ')

        print ""


#if __name__ == '__main__':
    #print points
    #graph = create_graph()


    #for x in range(-20,20):
    #    graph.set_impediment(x,0)

    # for x in range(10,50):
    #     graph.set_impediment(x,25)
    #
    # for x in range(0,30):
    #     graph.set_impediment(x,35)



    # # graph.print_distances()
    #visited, path = shortest_path(graph, '-9,-9', '9,9')
    #print_path(path)
