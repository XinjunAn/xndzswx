import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# ---------- 基于邻接矩阵的强连通判断 ----------
def is_strongly_connected_by_matrix(adj_matrix):
    """
    通过 Warshall 算法计算传递闭包，判断有向图是否强连通。
    参数: adj_matrix - 带有权重的邻接矩阵 (numpy 数组)
    返回: True (强连通) 或 False
    """
    n = adj_matrix.shape[0]
    # 构建布尔邻接矩阵：有边 (权重 > 0) 为 1，无自环情况也处理（对角元初始为 0）
    reach = np.where(adj_matrix > 0, 1, 0)  # 有边可直达

    #采用Warshall算法计算传递闭包，后续做介绍
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
            

    # 强连通要求：任意两点 i, j 彼此可达，即 reach 所有元素为 1（对角元也应为 1，因为自己可达自己）
    # 实际上 Warshall 得到的闭包对角元会自动变为 1（若存在回路）但未必，我们可手动置对角元为 1（每个节点到自身可达）
    for i in range(n):
        reach[i][i] = 1

    return np.all(reach == 1)

# ---------- 生成有向图 ----------
def generate_directed_graph(n, m):
    max_edges = n * (n - 1)
    if m > max_edges:
        raise ValueError(f"边数 m 不能超过 {max_edges}")
    all_edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    selected_edges = random.sample(all_edges, m)
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for u, v in selected_edges:
        randdata = random.randint(1, 10)
        w = 1 if randdata>=1 else 0
        G.add_edge(u, v, weight=w)
    return G
# ---------- 打印有向图矩阵 ----------
def print_matrix(matrix, title):
    print(f"\n{title}的邻接矩阵（整数权重）：")
    print(np.array2string(matrix.astype(int), separator=', '))
# ---------- 画出有向图示意结构----------
def draw_graph(G, title):
    plt.figure(figsize=(5, 5))
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=800, arrows=True, arrowstyle='-|>')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.axis('equal')
    plt.show()

# ---------- 主控制程序 ----------
if __name__ == "__main__":
    n = int(input("请输入顶点个数 n: "))
    m = int(input("请输入边的数目 m: "))

    try:
        G = generate_directed_graph(n, m)
        adj = nx.to_numpy_array(G, nodelist=range(n), weight='weight')
        print_matrix(adj, "有向图")

        # 使用矩阵迭代法判断强连通
        if is_strongly_connected_by_matrix(adj):
            print("\n该有向图是强连通图。")
        else:
            print("\n该有向图不是强连通图。")

        draw_graph(G, "Directed Graph (Matrix-based SC Check)")

    except ValueError as e:
        print("生成失败:", e)