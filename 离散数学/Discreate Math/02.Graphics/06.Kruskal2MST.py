import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

# ---------- 并查集，判断生成树中是否产生回路----------
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True

# ---------- Kruskal 算法 ----------
def kruskal(undirected_edges):
    n = max(max(u, v) for u, v, _ in undirected_edges) + 1
    
    #调用函数判断是否含有回路
    ds = DisjointSet(n)
    sorted_edges = sorted(undirected_edges, key=lambda e: e[2])
    mst = []
    total = 0
    for u, v, w in sorted_edges:
        if ds.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == n - 1:
                break
    return mst, total

# ---------- 生成带权有向图 ----------
def generate_directed_graph(n, m):
    if m < n - 1:
        raise ValueError(f"边数至少为 n-1={n-1} 才能构造生成树")
    max_edges = n * (n - 1) // 2
    if m > max_edges:
        raise ValueError(f"边数不能超过 {max_edges}（简单无向图的边数上限）")
    
    all_undirected = [(i, j) for i in range(n) for j in range(i+1, n)]
    selected_undirected = random.sample(all_undirected, m)
    
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for u, v in selected_undirected:
        w = random.randint(1, 20)
        if random.random() < 0.5:
            G.add_edge(u, v, weight=w)
        else:
            G.add_edge(v, u, weight=w)
    return G

# ---------- 辅助输出 ----------
def print_matrix(matrix, title):
    print(f"\n{title}的邻接矩阵（整数权重）：")
    print(np.array2string(matrix.astype(int), separator=', '))

# ---------- 绘制（含动画） ----------
def draw_original_and_mst_animated(G_dir, mst_edges):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 固定布局（使用圆形布局，便于观察）
    pos = nx.circular_layout(G_dir)
    
    # ---- 左侧：原图（一次性绘制，保持不变） ----
    ax1 = axes[0]
    nx.draw(G_dir, pos, ax=ax1, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=800, arrows=True, arrowstyle='-|>')
    edge_labels = nx.get_edge_attributes(G_dir, 'weight')
    nx.draw_networkx_edge_labels(G_dir, pos, edge_labels=edge_labels, ax=ax1)
    ax1.set_title("Directed Original Graph")
    
    # ---- 右侧：最小生成树（动画） ----
    ax2 = axes[1]
    ax2.set_title("Minimum Spanning Tree (Kruskal Animation)")
    # 先绘制节点
    nx.draw_networkx_nodes(G_dir, pos, ax=ax2, node_color='lightgreen', node_size=800)
    nx.draw_networkx_labels(G_dir, pos, ax=ax2)
    ax2.set_xlim(ax1.get_xlim())   # 保持坐标一致
    ax2.set_ylim(ax1.get_ylim())
    ax2.axis('off')
    
    plt.ion()   # 开启交互模式，允许动态更新
    plt.show()
    
    # 用于累积已添加的边（便于一次性画所有边及标签）
    accumulated_edges = []
    for idx, (u, v, w) in enumerate(mst_edges):
        accumulated_edges.append((u, v, w))
        
        # 清除上一次的边和标签（保留节点）
        # 简单方法：重新绘制所有累积的边
        ax2.clear()
        # 重绘节点和标签
        nx.draw_networkx_nodes(G_dir, pos, ax=ax2, node_color='lightgreen', node_size=800)
        nx.draw_networkx_labels(G_dir, pos, ax=ax2)
        ax2.set_title("Minimum Spanning Tree (Kruskal Animation)")
        ax2.set_xlim(ax1.get_xlim())
        ax2.set_ylim(ax1.get_ylim())
        ax2.axis('off')
        
        # 绘制当前所有累积的边（红色粗线）
        nx.draw_networkx_edges(G_dir, pos, ax=ax2,
                               edgelist=[(u, v) for u, v, _ in accumulated_edges],
                               edge_color='red', width=2)
        # 绘制边标签
        edge_labels_mst = {(u, v): w for u, v, w in accumulated_edges}
        nx.draw_networkx_edge_labels(G_dir, pos, edge_labels=edge_labels_mst, ax=ax2)
        
        # 更新图形并暂停1秒
        plt.draw()
        plt.pause(1)
    
    plt.ioff()   # 关闭交互模式
    plt.show()   # 保持窗口（阻塞）

# ---------- 主程序 ----------
if __name__ == "__main__":
    n = int(input("请输入顶点个数 n: "))
    m = int(input("请输入边的数目 m (需 ≥ n-1): "))
    
    try:
        G_dir = generate_directed_graph(n, m)
        adj = nx.to_numpy_array(G_dir, nodelist=range(n), weight='weight')
        print_matrix(adj, "有向图")
        
        # 提取无向边用于 Kruskal
        undirected_edges = [(u, v, w) for u, v, w in G_dir.edges(data='weight')]
        mst_edges, total_weight = kruskal(undirected_edges)
        
        print("\n最小生成树的边（无向）：")
        for u, v, w in mst_edges:
            print(f"  {u} -- {v}  权重={w}")
        print(f"总权重 = {total_weight}")
        
        draw_original_and_mst_animated(G_dir, mst_edges)
        
    except ValueError as e:
        print("生成失败:", e)