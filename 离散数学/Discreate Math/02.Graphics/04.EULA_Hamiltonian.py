import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

# ---------- 欧拉回路算法（Hierholzer，自行实现） ----------
def find_eulerian_circuit(graph):
    """
    返回欧拉回路边的列表，每条边以 (u, v) 形式表示（无向边按照遍历顺序）。
    要求：graph 所有顶点度数为偶数且连通（除孤立点）。
    """
    # 复制图，因为需要删除边
    g = graph.copy()
    circuit = []
    # 栈用于 Hierholzer 算法
    stack = []
    # 任选起点（第一个节点）
    start = list(g.nodes())[0]
    stack.append(start)
    while stack:
        v = stack[-1]
        if g.degree(v) == 0:
            circuit.append(stack.pop())
        else:
            # 取一个邻居
            u = next(iter(g.neighbors(v)))
            g.remove_edge(v, u)
            stack.append(u)
    # circuit 存储的是顶点序列，转换为边序列
    edges = []
    for i in range(len(circuit)-1):
        edges.append((circuit[i], circuit[i+1]))
    # 欧拉回路是闭合的，circuit[0] == circuit[-1]
    return edges

# ---------- 哈密尔顿回路搜索（回溯） ----------
def hamiltonian_circuit(graph):
    """
    搜索哈密尔顿回路，返回顶点序列（list），若不存在返回 None。
    """
    n = graph.number_of_nodes()
    nodes = list(graph.nodes())
    adj = {u: set(graph.neighbors(u)) for u in nodes}
    
    def backtrack(path, visited):
        if len(path) == n:
            # 检查能否回到起点
            if path[0] in adj[path[-1]]:
                return path + [path[0]]
            return None
        last = path[-1]
        for neighbor in adj[last]:
            if neighbor not in visited:
                visited.add(neighbor)
                res = backtrack(path + [neighbor], visited)
                if res:
                    return res
                visited.remove(neighbor)
        return None
    
    for start in nodes:
        res = backtrack([start], {start})
        if res:
            return res
    return None

# ---------- 生成连通的无向图 ----------
def generate_connected_graph(n, m):
    if m < n - 1:
        raise ValueError(f"边数至少为 n-1={n-1} 才能连通")
    max_edges = n * (n - 1) // 2
    if m > max_edges:
        raise ValueError(f"边数不能超过 {max_edges}")
    
    # 先生成一棵随机树
    nodes = list(range(n))
    random.shuffle(nodes)
    tree_edges = []
    connected = {nodes[0]}
    remaining = set(nodes[1:])
    while remaining:
        u = random.choice(list(connected))
        v = random.choice(list(remaining))
        tree_edges.append((u, v))
        connected.add(v)
        remaining.remove(v)
    
    # 添加剩余的随机边
    all_possible = set((i, j) for i in range(n) for j in range(i+1, n))
    existing = set((u, v) if u < v else (v, u) for u, v in tree_edges)
    possible_extra = list(all_possible - existing)
    extra_needed = m - (n - 1)
    extra_edges = random.sample(possible_extra, extra_needed)
    
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for u, v in tree_edges + extra_edges:
        G.add_edge(u, v)
    return G

# ---------- 打印邻接矩阵 ----------
def print_matrix(graph, title):
    adj = nx.to_numpy_array(graph, nodelist=sorted(graph.nodes()))
    print(f"\n{title}的邻接矩阵：")
    print(np.array2string(adj.astype(int), separator=', '))

# ---------- 绘制原图和回路 ----------
def draw_graph_and_circuits(G, euler_edges=None, hamilton_path=None):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    pos = nx.spring_layout(G, seed=42)   # 固定布局便于比较
    
    # 左侧：欧拉回路
    ax1 = axes[0]
    nx.draw_networkx_nodes(G, pos, ax=ax1, node_color='lightblue', node_size=800)
    nx.draw_networkx_labels(G, pos, ax=ax1)
    nx.draw_networkx_edges(G, pos, ax=ax1, edge_color='gray', alpha=0.5)  # 背景边
    if euler_edges:
        nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=euler_edges,
                               edge_color='green', width=3)
        ax1.set_title("Eulerian Circuit (green)")
    else:
        ax1.set_title("Not Eulerian (no circuit)")
    ax1.axis('off')
    
    # 右侧：哈密尔顿回路
    ax2 = axes[1]
    nx.draw_networkx_nodes(G, pos, ax=ax2, node_color='lightblue', node_size=800)
    nx.draw_networkx_labels(G, pos, ax=ax2)
    nx.draw_networkx_edges(G, pos, ax=ax2, edge_color='gray', alpha=0.5)
    if hamilton_path:
        # 将顶点路径转换为有向边序列（用于箭头显示）
        hamilton_edges = [(hamilton_path[i], hamilton_path[i+1]) for i in range(len(hamilton_path)-1)]
        nx.draw_networkx_edges(G, pos, ax=ax2, edgelist=hamilton_edges,
                               edge_color='red', width=3, arrowstyle='-|>', arrows=True,
                               connectionstyle='arc3,rad=0.1')  # 弯箭头避免重叠
        ax2.set_title("Hamiltonian Circuit (red)")
    else:
        ax2.set_title("Not Hamiltonian (no circuit)")
    ax2.axis('off')
    
    plt.tight_layout()
    plt.show()

# ---------- 主程序 ----------
if __name__ == "__main__":
    n = int(input("请输入顶点个数 n（建议≤12）: "))
    m = int(input(f"请输入边的数目 m（≥{n-1}）: "))
    
    try:
        G = generate_connected_graph(n, m)
        print_matrix(G, "无向图")
        
        # --- 欧拉判断 ---
        degrees = dict(G.degree())
        is_eulerian = all(d % 2 == 0 for d in degrees.values())
        euler_edges = None
        if is_eulerian:
            euler_edges = find_eulerian_circuit(G)
            print("\n该图是欧拉图（存在欧拉回路）。")
            print("欧拉回路边序列：", euler_edges)
        else:
            print("\n该图不是欧拉图（存在奇数度顶点）。")
        
        # --- 哈密尔顿判断 ---
        ham_path = hamiltonian_circuit(G)
        if ham_path:
            print("该图是哈密尔顿图（存在哈密尔顿回路）。")
            print("哈密尔顿回路顶点序列：", ham_path)
        else:
            print("该图不是哈密尔顿图（未找到哈密尔顿回路）。")
        
        # 绘图
        draw_graph_and_circuits(G, euler_edges, ham_path)
        
    except ValueError as e:
        print("生成失败:", e)