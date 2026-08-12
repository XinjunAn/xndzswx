import random
import heapq
import networkx as nx
import matplotlib.pyplot as plt

def generate_random_connected_graph(num_vertices, max_weight=20, edge_prob=0.6):
    """
    随机生成一个带权无向连通图，返回邻接矩阵（二维列表）。
    """
    INF = float('inf')
    graph = [[INF] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        graph[i][i] = 0

    # 1. 建立随机生成树，保证连通性
    vertices = list(range(num_vertices))
    random.shuffle(vertices)
    for i in range(1, num_vertices):
        u = vertices[i]
        v = random.choice(vertices[:i])
        weight = random.randint(1, max_weight)
        graph[u][v] = weight
        graph[v][u] = weight

    # 2. 随机添加额外边
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if graph[i][j] == INF and random.random() < edge_prob:
                weight = random.randint(1, max_weight)
                graph[i][j] = weight
                graph[j][i] = weight

    return graph


def print_matrix(graph):
    """友好地打印邻接矩阵，∞ 显示为 '-'"""
    n = len(graph)
    print("    ", end="")
    for j in range(n):
        print(f"{j:>4}", end="")
    print()
    for i in range(n):
        print(f"{i:>4}", end="")
        for j in range(n):
            if graph[i][j] == float('inf'):
                print("   -", end="")
            else:
                print(f"{graph[i][j]:>4}", end="")
        print()


def prim_basic(graph, start=0):
    """Prim 朴素实现 O(V^2)，返回 (mst_edges, total_weight)"""
    n = len(graph)
    key = [float('inf')] * n
    parent = [-1] * n
    in_mst = [False] * n

    key[start] = 0
    parent[start] = -1

    for _ in range(n):
        u = -1
        min_key = float('inf')
        for v in range(n):
            if not in_mst[v] and key[v] < min_key:
                min_key = key[v]
                u = v

        if u == -1:
            break

        in_mst[u] = True

        for v in range(n):
            if (not in_mst[v] and 
                graph[u][v] != float('inf') and 
                graph[u][v] < key[v]):
                key[v] = graph[u][v]
                parent[v] = u

    mst_edges = []
    total_weight = 0
    for v in range(n):
        if parent[v] != -1:
            u = parent[v]
            w = graph[u][v]
            mst_edges.append((u, v, w))
            total_weight += w

    return mst_edges, total_weight


def prim_heap(graph, start=0):
    """Prim 堆优化 O(E log V)，返回 (mst_edges, total_weight)"""
    n = len(graph)
    key = [float('inf')] * n
    parent = [-1] * n
    in_mst = [False] * n

    key[start] = 0
    heap = [(0, start)]

    while heap:
        cur_key, u = heapq.heappop(heap)
        if in_mst[u]:
            continue
        in_mst[u] = True

        for v in range(n):
            w = graph[u][v]
            if w != float('inf') and not in_mst[v] and w < key[v]:
                key[v] = w
                parent[v] = u
                heapq.heappush(heap, (w, v))

    mst_edges = []
    total_weight = 0
    for v in range(n):
        if parent[v] != -1:
            u = parent[v]
            total_weight += graph[u][v]
            mst_edges.append((u, v, graph[u][v]))

    return mst_edges, total_weight


def draw_graph_and_mst(graph, mst_edges, title="Graph & Minimum Spanning Tree"):
    """
    绘制原始图并高亮 MST。
    所有边都标注权重：非 MST 边用灰色小字，MST 边用红色粗字。
    """
    n = len(graph)
    G = nx.Graph()
    G.add_nodes_from(range(n))

    # 建立所有边的权重字典（无向边只存一次）
    edge_labels_all = {}
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] != float('inf'):
                edge_labels_all[(i, j)] = graph[i][j]
                G.add_edge(i, j, weight=graph[i][j])

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 7))

    # 1. 画所有边（灰色细线）
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray', width=1.5)

    # 2. 画所有边的权重（灰色小字）
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_all,
                                 font_size=8, font_color='gray', alpha=0.7)

    # 3. 提取 MST 边用于高亮
    mst_labels = {}
    mst_edgelist = []
    for u, v, w in mst_edges:
        # 统一顺序，确保与 edge_labels_all 的键一致
        if (u, v) in edge_labels_all:
            mst_labels[(u, v)] = w
            mst_edgelist.append((u, v))
        elif (v, u) in edge_labels_all:
            mst_labels[(v, u)] = w
            mst_edgelist.append((v, u))
        else:
            # 理论上不会发生
            mst_labels[(u, v)] = w
            mst_edgelist.append((u, v))

    # 4. 画 MST 边（红色粗线）
    nx.draw_networkx_edges(G, pos, edgelist=mst_edgelist,
                           edge_color='red', width=3.5, alpha=0.9)

    # 5. 画 MST 边的权重（红色粗字，覆盖在灰色上方）
    nx.draw_networkx_edge_labels(G, pos, edge_labels=mst_labels,
                                 font_size=10, font_weight='bold',
                                 font_color='red')

    # 6. 画节点和标签
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color='lightblue',
                           edgecolors='black', linewidths=1.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


# ========== 主程序 ==========
if __name__ == "__main__":
    random.seed(42)
    V = 6
    max_w = 20
    density = 0.4

    print(f"随机生成 {V} 个顶点的带权连通图（最大权重 {max_w}，额外边密度 {density}）\n")
    graph = generate_random_connected_graph(V, max_weight=max_w, edge_prob=density)

    print("邻接矩阵（'-' 表示无边）：")
    print_matrix(graph)

    edges_basic, weight_basic = prim_basic(graph, start=0)
    print("\n========== Prim (朴素 O(V^2)) ==========")
    print("MST 边（u - v : weight）：")
    for u, v, w in sorted(edges_basic):
        print(f"  {u} - {v} : {w}")
    print(f"最小生成树总权重：{weight_basic}")

    edges_heap, weight_heap = prim_heap(graph, start=0)
    print("\n========== Prim (堆优化 O(E log V)) ==========")
    print("MST 边（u - v : weight）：")
    for u, v, w in sorted(edges_heap):
        print(f"  {u} - {v} : {w}")
    print(f"最小生成树总权重：{weight_heap}")

    assert weight_basic == weight_heap, "两种实现总权重不一致！"
    print("\n✅ 两种实现得到相同的最小生成树总权重。")

    # 绘制图形，所有边均显示权值
    draw_graph_and_mst(graph, edges_basic, "Minimum Spanning Tree (all weights shown)")