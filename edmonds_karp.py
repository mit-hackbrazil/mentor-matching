class Edge:
    def __init__(self, cap, flow):
        self.cap = cap
        self.flow = flow

    def left(self):
        return self.cap - self.flow


def max_flow(src, dst, graph):
    flow = 0
    while True:
        path = bfs(src, dst, graph)
        if not path:
            break
        edges = zip(path[:-1], path[1:])

        df = min([graph[e].left() for e in edges])
        for s, t in edges:
            graph[(s, t)].flow += df
            graph[(t, s)].flow -= df

        flow += df

    return flow

def bfs(src, dst, graph):
    queue = [[src]]
    visited = []
    res = None
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == dst:
            return path

        if node in visited:
            continue

        visited.append(node)
        for s, t in graph:
            if s != node:
                continue
            e = graph[(s, t)]
            if e.cap > e.flow:
                queue.append(path + [t])

    return None



