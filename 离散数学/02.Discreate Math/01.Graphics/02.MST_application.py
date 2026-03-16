#图论案例—— 校园光纤网络铺设方案
import networkx as nx
import matplotlib.pyplot as plt

def teach_mst_case():
    # 1. 定义节点（建筑）
    buildings = ['Admin', 'Library', 'Classroom', 'Dorm', 'Canteen']
    
    # 2. 定义边和权重（路径成本，单位：万元）
    # 格式: (起点, 终点, 权重)
    # 这是一个全连接图或者部分连接图，表示潜在的施工路径
    edges = [
        ('Admin', 'Library', 4),
        ('Admin', 'Classroom', 2),
        ('Admin', 'Canteen', 10),
        ('Library', 'Classroom', 3),
        ('Library', 'Dorm', 8),
        ('Classroom', 'Dorm', 7),
        ('Classroom', 'Canteen', 6),
        ('Dorm', 'Canteen', 5),
        ('Library', 'Canteen', 9) # 假设这是一条很远的路
    ]

    # 3. 创建图结构
    G = nx.Graph()
    G.add_nodes_from(buildings)
    G.add_weighted_edges_from(edges)

    # 4. 计算最小生成树 (MST) - 使用 Kruskal 算法思想
    mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

    # --- 以下是可视化绘图代码 ---
    plt.figure(figsize=(14, 6))

    # 设置布局 (固定位置以便对比)
    pos = nx.spring_layout(G, seed=42) 

    # === 左图：原始所有可能的路径 ===
    plt.subplot(1, 2, 1)
    plt.title("Original Potential Topology (High Redundancy)", fontsize=12)
    
    # 绘制所有边
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edge_color='gray', style='dashed')
    nx.draw_networkx_labels(G, pos)
    
    # 标注权重
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # === 右图：最小生成树（最优布线方案） ===
    plt.subplot(1, 2, 2)
    plt.title(f"Optimized Topology (MST)\nMin Cost: {mst.size(weight='weight')}0k", fontsize=12)
    
    # 绘制背景（淡色的原始路径，表示被放弃的线路）
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgreen')
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', style=':', alpha=0.5)
    
    # 高亮绘制MST的边
    nx.draw_networkx_edges(mst, pos, edge_color='red', width=2.5)
    nx.draw_networkx_labels(G, pos)
    
    # 标注MST边的权重
    mst_edge_labels = nx.get_edge_attributes(mst, 'weight')
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=mst_edge_labels, font_color='red')

    plt.tight_layout()
    plt.show()

    # 输出具体方案
    print("=== 最终铺设方案 ===")
    total_cost = 0
    for u, v, d in mst.edges(data=True):
        print(f"连接 [{u}] 和 [{v}]，成本: {d['weight']} 万元")
        total_cost += d['weight']
    print(f"-----------------------")
    print(f"总计最低成本: {total_cost} 万元")

if __name__ == "__main__":
    teach_mst_case()