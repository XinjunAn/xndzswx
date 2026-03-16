#图论案例——数据中心巡检机器人的“双重任务”
import networkx as nx
import matplotlib.pyplot as plt

def teach_euler_hamilton():
    # === 创建一个既包含欧拉回路又包含哈密尔顿回路的图 ===
    # 典型的 "八面体图" (Octahedral Graph) 是一个很好的例子
    # 它的每个节点度数都是4（偶数 -> 欧拉图）
    # 它也是连通的，且包含经过所有点的圈（哈密尔顿图）
    G = nx.octahedral_graph()
    
    # 重新命名节点，模拟服务器名称
    mapping = {0:'Srv_A', 1:'Srv_B', 2:'Srv_C', 3:'Srv_D', 4:'Srv_E', 5:'Srv_F'}
    G = nx.relabel_nodes(G, mapping)

    # 设置画图布局
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(16, 7))

    # ==========================================
    # 场景 1: 线路质检模式 (欧拉回路 - 关注边)
    # ==========================================
    plt.subplot(1, 2, 1)
    plt.title("Task A: Link Inspection (Eulerian Circuit)\nVisit every EDGE exactly once", fontsize=12)
    
    # 1. 检查是否是欧拉图
    if nx.is_eulerian(G):
        # 2. 计算欧拉回路
        euler_circuit = list(nx.eulerian_circuit(G))
        
        # 绘制底图
        nx.draw_networkx_nodes(G, pos, node_size=600, node_color='lightgray')
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3)
        
        # 可视化路径顺序
        # 我们用渐变色或者带数字的箭头来表示走的顺序
        edge_colors = range(len(euler_circuit))
        nx.draw_networkx_edges(
            G, pos,
            edgelist=euler_circuit,
            edge_color=edge_colors,
            edge_cmap=plt.cm.cool, # 颜色从冷到暖表示顺序
            width=2.5,
            arrows=True,
            arrowstyle='-|>'
        )
        
        # 在图下方打印路径文字
        path_str = " -> ".join([u for u, v in euler_circuit] + [euler_circuit[-1][1]])
        print(f"=== 任务 A (欧拉) 路径 ===")
        print(f"特点：不重复走任何一条线")
        print(f"路径: {path_str}\n")
    else:
        plt.text(0,0, "Graph is not Eulerian!", fontsize=20)

    # ==========================================
    # 场景 2: 数据采集模式 (哈密尔顿回路 - 关注点)
    # ==========================================
    plt.subplot(1, 2, 2)
    plt.title("Task B: Data Collection (Hamiltonian Cycle)\nVisit every NODE exactly once", fontsize=12)
    
    # NetworkX 没有直接求哈密尔顿回路的简单函数(因为是NP难)，
    # 但对于这个特定图，我们知道一个合法的哈密尔顿路径。
    # 这里我们手动模拟一条哈密尔顿回路用于演示
    # 路径: A -> B -> C -> E -> F -> D -> A
    hamilton_path_edges = [
        ('Srv_A', 'Srv_B'), ('Srv_B', 'Srv_C'), ('Srv_C', 'Srv_E'),
        ('Srv_E', 'Srv_F'), ('Srv_F', 'Srv_D'), ('Srv_D', 'Srv_A')
    ]
    
    # 绘制底图
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color='lightgreen')
    nx.draw_networkx_labels(G, pos)
    # 绘制所有边作为背景
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3, style='dashed')
    
    # 高亮绘制哈密尔顿回路
    nx.draw_networkx_edges(
        G, pos,
        edgelist=hamilton_path_edges,
        edge_color='red',
        width=3.0,
        arrows=True
    )
    
    print(f"=== 任务 B (哈密尔顿) 路径 ===")
    print(f"特点：访问所有服务器，很多网线并不需要走")
    path_nodes = [u for u,v in hamilton_path_edges] + [hamilton_path_edges[-1][1]]
    print(f"路径: {' -> '.join(path_nodes)}")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    teach_euler_hamilton()