#调用随机数
import random
import numpy as np
#调用networkx包，构造图结构
import networkx as nx
import matplotlib.pyplot as plt

def generate_directed_graph(n, m):
    """生成有向图，返回图对象和邻接矩阵"""
    max_edges = n * (n - 1)
    if m > max_edges:
        raise ValueError(f"边数 m 不能超过 {max_edges}（n*(n-1)）")
    all_edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    selected_edges = random.sample(all_edges, m)
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for u, v in selected_edges:
        w = random.randint(1, 10)
        G.add_edge(u, v, weight=w)
    adj_matrix = nx.to_numpy_array(G, nodelist=range(n), weight='weight')
    return G, adj_matrix

def generate_undirected_graph(n, m):
    """生成无向图，返回图对象和邻接矩阵"""
    max_edges = n * (n - 1) // 2
    if m > max_edges:
        raise ValueError(f"边数 m 不能超过 {max_edges}（n*(n-1)/2）")
    all_edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    selected_edges = random.sample(all_edges, m)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for u, v in selected_edges:
        w = random.randint(1, 10)
        G.add_edge(u, v, weight=w)
    adj_matrix = nx.to_numpy_array(G, nodelist=range(n), weight='weight')
    return G, adj_matrix

def print_matrix(matrix, title):
    """格式化打印矩阵"""
    print(f"\n{title}的邻接矩阵（整数权重）：")
    print(np.array2string(matrix.astype(int), separator=', '))

def draw_graphs_together(G_dir, G_und):
    """在同一界面绘制有向图和无向图"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 有向图（左）
    ax1 = axes[0]
    pos_dir = nx.circular_layout(G_dir)
    nx.draw(G_dir, pos_dir, ax=ax1, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=800, arrows=True, arrowstyle='-|>')
    edge_labels_dir = nx.get_edge_attributes(G_dir, 'weight')
    nx.draw_networkx_edge_labels(G_dir, pos_dir, edge_labels=edge_labels_dir, ax=ax1)
    ax1.set_title("Directed Graph (Integer Weights)")
    
    # 无向图（右）
    ax2 = axes[1]
    pos_und = nx.spring_layout(G_und, seed=42)
    nx.draw(G_und, pos_und, ax=ax2, with_labels=True, node_color='lightgreen',
            edge_color='gray', node_size=800)
    edge_labels_und = nx.get_edge_attributes(G_und, 'weight')
    nx.draw_networkx_edge_labels(G_und, pos_und, edge_labels=edge_labels_und, ax=ax2)
    ax2.set_title("Undirected Graph (Integer Weights)")
    
    plt.tight_layout()
    plt.show()

# ----------------- 主程序 -----------------
if __name__ == "__main__":
    n = int(input("请输入顶点个数 n: "))
    m = int(input("请输入边的数目 m: "))

    try:
        G_dir, mat_dir = generate_directed_graph(n, m)
        print_matrix(mat_dir, "有向图")
        
        G_und, mat_und = generate_undirected_graph(n, m)
        print_matrix(mat_und, "无向图")
        
        # 在同一个窗口并排绘制两幅图
        draw_graphs_together(G_dir, G_und)
        
    except ValueError as e:
        print("生成失败:", e)