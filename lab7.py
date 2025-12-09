from collections import deque
import heapq
import networkx as nx
import matplotlib.pyplot as plt

def to_matrix(state):
    return [state[0:3], state[3:6], state[6:9]]

def get_neighbors(state):
    moves = []
    zero_index = state.index(0)
    x, y = zero_index // 3, zero_index % 3
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx,dy in directions:
        nx_, ny_ = x + dx, y + dy
        if 0 <= nx_ < 3 and 0 <= ny_ < 3:
            new_index = nx_ * 3 + ny_
            s = list(state)
            s[zero_index], s[new_index] = s[new_index], s[zero_index]
            moves.append(tuple(s))
    return moves

def bfs(start, goal):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur = queue.popleft()
        if cur == goal:
            return visited
        for nxt in get_neighbors(cur):
            if nxt not in visited:
                visited[nxt] = cur
                queue.append(nxt)
    return None

def manhattan(state, goal):
    dist = 0
    for num in range(1, 9):
        x1, y1 = divmod(state.index(num), 3)
        x2, y2 = divmod(goal.index(num), 3)
        dist += abs(x1 - x2) + abs(y1 - y2)
    return dist

def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    visited = {start: None}
    g = {start: 0}

    while open_set:
        _, cur = heapq.heappop(open_set)
        if cur == goal:
            return visited
        for nxt in get_neighbors(cur):
            new_cost = g[cur] + 1
            if nxt not in g or new_cost < g[nxt]:
                g[nxt] = new_cost
                f = new_cost + manhattan(nxt, goal)
                visited[nxt] = cur
                heapq.heappush(open_set, (f, nxt))
    return None

def reconstruct_path(visited, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = visited[cur]
    return list(reversed(path))

def reverse_bfs(goal, start):
    return bfs(goal, start)

def build_graph(start, limit=20):
    G = nx.DiGraph()
    queue = deque([start])
    visited = set([start])
    count = 0

    while queue and count < limit:
        cur = queue.popleft()
        for nxt in get_neighbors(cur):
            G.add_edge(cur, nxt)
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
                count += 1
    return G

def visualize_graph(G):
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False, node_size=300, arrows=False)
    plt.title("Граф переходов состояния 8-puzzle")
    plt.show()

start = (1,2,3,4,0,6,7,5,8)
goal = (1,2,3,4,5,6,7,8,0)

print("BFS поиск...")
visited_bfs = bfs(start, goal)
path_bfs = reconstruct_path(visited_bfs, goal)
print("Шагов BFS:", len(path_bfs)-1)

print("\nA* поиск...")
visited_astar = a_star(start, goal)
path_astar = reconstruct_path(visited_astar, goal)
print("Шагов A*:", len(path_astar)-1)

print("\nСтрою граф переходов (20 состояний)...")
G = build_graph(start, limit=20)
visualize_graph(G)