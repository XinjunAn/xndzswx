#数理逻辑案例——网络工程中的“高可用性(HA)拓扑”与逻辑运算

import networkx as nx
import matplotlib.pyplot as plt

def visualize_network_logic(isp_a_status, isp_b_status, fw_status):
    # 1. 创建有向图
    G = nx.DiGraph()
    
    # 2. 定义节点位置 (为了画出漂亮的拓扑)
    pos = {
        'Internet': (1, 3),
        'ISP_A': (0, 2),
        'ISP_B': (2, 2),
        'Firewall': (1, 1),
        'Server': (1, 0)
    }
    
    # 3. 添加节点
    G.add_nodes_from(pos.keys())
    
    # 4. 定义边的逻辑状态
    # 逻辑：ISP链路通不通，取决于ISP本身的状态
    colors = []
    
    # 边1: Internet -> ISP_A
    G.add_edge('Internet', 'ISP_A')
    colors.append('green' if isp_a_status else 'red')
    
    # 边2: Internet -> ISP_B
    G.add_edge('Internet', 'ISP_B')
    colors.append('green' if isp_b_status else 'red')
    
    # 边3: ISP_A -> Firewall
    G.add_edge('ISP_A', 'Firewall')
    colors.append('green' if isp_a_status else 'red')
    
    # 边4: ISP_B -> Firewall
    G.add_edge('ISP_B', 'Firewall')
    colors.append('green' if isp_b_status else 'red')
    
    # 核心逻辑: Firewall -> Server 通不通？
    # 取决于: (ISP_A 或 ISP_B) 并且 Firewall活着
    internet_access = (isp_a_status or isp_b_status)
    final_link_status = internet_access and fw_status
    
    G.add_edge('Firewall', 'Server')
    colors.append('green' if final_link_status else 'red')

    # 5. 绘图
    plt.figure(figsize=(8, 6))
    plt.title(f"Network Logic: (A={isp_a_status} ∨ B={isp_b_status}) ∧ FW={fw_status}\n"
              f"System Status: {'ONLINE' if final_link_status else 'OFFLINE'}", 
              fontsize=14, color='green' if final_link_status else 'red')
    
    # 画节点
    node_colors = ['lightgray' if n != 'Server' else ('lightgreen' if final_link_status else 'salmon') for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color=node_colors, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # 画边 (带颜色)
    nx.draw_networkx_edges(G, pos, edge_color=colors, width=3, arrowsize=20, arrowstyle='->')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# === 教学演示：修改这里的 True/False 来模拟不同故障 ===
# 场景 1: 完美状态
print("Case 1: All Systems Go")
visualize_network_logic(isp_a_status=True, isp_b_status=True, fw_status=True)

# 场景 2: ISP A 挂了，但网络依然通 (体现逻辑或的冗余性)
# print("Case 2: ISP Redundancy works")
# visualize_network_logic(isp_a_status=False, isp_b_status=True, fw_status=True)

# 场景 3: 防火墙挂了 (体现逻辑与的阻断性 - 单点故障)
# print("Case 3: Single Point of Failure")
# visualize_network_logic(isp_a_status=True, isp_b_status=True, fw_status=False)