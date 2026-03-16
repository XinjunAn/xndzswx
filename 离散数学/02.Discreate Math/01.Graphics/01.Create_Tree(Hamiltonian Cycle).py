#图论的应用——研讨会上的座位问题
import networkx as nx
import matplotlib.pyplot as plt

def solve_round_table():
    # 1. 定义人员及其掌握的语言 (使用集合方便求交集)
    people_languages = {
        'A': {'English'},
        'B': {'English', 'Chinese'},
        'C': {'English', 'Italian', 'Russian'},
        'D': {'Japanese', 'Chinese'},
        'E': {'German', 'Italian'},
        'F': {'French', 'Japanese', 'Russian'},
        'G': {'French', 'German'}
    }
    
    people_names = list(people_languages.keys())
    
    # 2. 构建图结构
    G = nx.Graph()
    G.add_nodes_from(people_names)
    
    # 添加边：如果两人有共同语言，则连线
    # 同时记录他们共同的语言作为边的属性
    for i in range(len(people_names)):
        for j in range(i + 1, len(people_names)):
            p1 = people_names[i]
            p2 = people_names[j]
            
            # 求语言交集
            common_langs = people_languages[p1].intersection(people_languages[p2])
            
            if common_langs:
                # 将集合转为字符串，如 "English"
                lang_str = "/".join(common_langs)
                G.add_edge(p1, p2, language=lang_str)

    # 3. 寻找哈密尔顿回路 (DFS 回溯法)
    # NetworkX 没有内置通用的哈密尔顿回路查找函数（因为是NP完全问题），
    # 但对于只有7个节点的图，简单的回溯法秒出结果。
    
    def find_hamiltonian_cycle(graph):
        nodes = list(graph.nodes())
        start_node = nodes[0]
        path = [start_node]
        
        def backtrack(current_node):
            # 如果路径长度等于节点数，且当前节点能回到起点，则找到回路
            if len(path) == len(nodes):
                if graph.has_edge(current_node, start_node):
                    return path + [start_node] # 闭合回路
                else:
                    return None
            
            # 遍历邻居
            for neighbor in graph.neighbors(current_node):
                if neighbor not in path:
                    path.append(neighbor)
                    result = backtrack(neighbor)
                    if result:
                        return result
                    path.pop() # 回溯
            return None

        return backtrack(start_node)

    cycle_nodes = find_hamiltonian_cycle(G)

    # 4. 结果输出与可视化
    plt.figure(figsize=(10, 8))
    
    # 使用圆形布局 (Round Table)
    pos = nx.circular_layout(G)
    
    if cycle_nodes:
        print("=== 成功找到圆桌座位安排方案！===")
        # 生成边的列表用于画图
        cycle_edges = []
        arrangement_str = ""
        
        for k in range(len(cycle_nodes) - 1):
            u, v = cycle_nodes[k], cycle_nodes[k+1]
            cycle_edges.append((u, v))
            # 获取共同语言
            lang = G[u][v]['language']
            arrangement_str += f"{u} --({lang})--> "
            
        print(arrangement_str + cycle_nodes[-1]) # 打印文本方案
        
        # --- 绘图 ---
        plt.title("Round Table Seating Plan (Hamiltonian Cycle)", fontsize=14)
        
        # 1. 画所有可能的交流路径 (浅灰色背景)
        nx.draw_networkx_edges(G, pos, edge_color='lightgray', style='dashed', alpha=0.5)
        
        # 2. 画节点
        nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='skyblue')
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        
        # 3. 画座位安排路径 (红色粗线)
        nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, edge_color='red', width=3)
        
        # 4. 在红线上标注共同语言
        # 只提取回路上的边的标签
        cycle_labels = {(u,v): G[u][v]['language'] for u,v in cycle_edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=cycle_labels, font_color='red', font_size=10)
        
    else:
        print("无法安排座位：图中不存在哈密尔顿回路。")
        plt.title("No Solution Found")
        nx.draw(G, pos, with_labels=True)

    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    solve_round_table()