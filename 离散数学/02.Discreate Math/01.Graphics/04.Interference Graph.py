#图论案例——无线基站的频谱（频道）分配
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def teach_coloring_case():
    # 1. 模拟工程场景：8个基站的坐标 (x, y)
    # 假设这是园区地图上的坐标
    stations = {
        0: (0, 0), 1: (2, 1), 2: (1, 3), 3: (4, 2),
        4: (5, 4), 5: (3, 5), 6: (6, 0), 7: (2, -2)
    }
    
    # 2. 建立干扰模型
    # 规则：如果两个基站距离小于 3.5 单位，则视为会发生干扰，必须连边
    G = nx.Graph()
    G.add_nodes_from(stations.keys())
    
    dist_threshold = 3.5
    for i in stations:
        for j in stations:
            if i < j:
                # 计算欧几里得距离
                pos_i = np.array(stations[i])
                pos_j = np.array(stations[j])
                dist = np.linalg.norm(pos_i - pos_j)
                if dist < dist_threshold:
                    G.add_edge(i, j)

    # 3. 核心算法：贪心着色 (Greedy Coloring)
    # strategy='largest_first' 意味着先处理连接数最多的基站，这是工程上的优选策略
    coloring_result = nx.coloring.greedy_color(G, strategy='largest_first')
    
    # coloring_result 格式如: {0: 0, 1: 1, 2: 0...} 节点:颜色ID
    
    # 统计用了多少种颜色（频道）
    num_colors = max(coloring_result.values()) + 1
    print(f"=== 分配结果 ===")
    print(f"最少需要频道数量: {num_colors}")
    print(f"具体分配: {coloring_result}")

    # 4. 可视化绘图
    plt.figure(figsize=(14, 6))
    
    # 定义颜色映射表 (用于画图显示)
    color_map_hex = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1']
    # 将算法结果的 0,1,2... 映射为具体的 Hex 颜色
    node_colors = [color_map_hex[coloring_result[node]] for node in G.nodes()]

    pos = stations # 使用真实的地理坐标作为布局

    # === 左图：物理布局与干扰关系 ===
    plt.subplot(1, 2, 1)
    plt.title("Interference Graph (Physical Layout)", fontsize=12)
    # 画点（统一灰色）
    nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=600, edgecolors='black')
    # 画边（代表冲突）
    nx.draw_networkx_edges(G, pos, edge_color='red', style='dashed')
    nx.draw_networkx_labels(G, pos)
    plt.axis('off')

    # === 右图：频道分配方案 ===
    plt.subplot(1, 2, 2)
    plt.title(f"Channel Allocation Solution\nTotal Channels Used: {num_colors}", fontsize=12)
    
    # 画点（使用分配好的颜色）
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600, edgecolors='black')
    # 画边
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_color='white')
    
    # 创建图例
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=f'Channel {i+1}',
                          markerfacecolor=color_map_hex[i], markersize=10)
                          for i in range(num_colors)]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    teach_coloring_case()