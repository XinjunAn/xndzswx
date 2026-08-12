#----------------------------------------------------
#Hierholzer 算法（又称“套圈法”）是一种用于在欧拉图(所有顶点度数均为偶数)中寻找 欧拉回路
#----------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx          # 仅用于绘图，不调用图算法

# ---------- 1. 设置中文字体（可选，若系统无中文字体可改用英文标题） ----------
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 2. 构建完全图 K5（既是欧拉图，又有欧拉回路） ----------
n = 5
adj = {i: [j for j in range(n) if j != i] for i in range(n)}   # 邻接表（无向图）
G = nx.complete_graph(n)          # 仅用于绘图
pos = nx.spring_layout(G, seed=42) # 固定布局，保证可复现

# ---------- 3. Hierholzer 算法（迭代版，无递归） ----------
def hierholzer(adj):
    """
    返回欧拉回路的顶点序列（起点与终点相同）。
    算法原地修改图的副本，不破坏原始邻接表。
    """
    # 复制邻接表，以便删除边
    graph = {v: adj[v][:] for v in adj}
    
    # 检查是否所有顶点度数为偶数（欧拉图前提）
    for v in graph:
        if len(graph[v]) % 2 != 0:
            raise ValueError(f"顶点 {v} 的度数为奇数，不存在欧拉回路。")
    
    stack = []
    circuit = []
    start = 0                      # 任选起点（顶点0）
    curr = start
    stack.append(curr)
    
    while stack:
        if graph[curr]:            # 当前顶点还有未遍历的边
            stack.append(curr)     # 记录回溯点
            nxt = graph[curr].pop() # 取一个邻居
            # 删除反向边（无向图）
            graph[nxt].remove(curr)
            curr = nxt             # 前进
        else:
            # 无路可走，闭合当前环，回溯
            circuit.append(curr)
            curr = stack.pop()
    
    circuit.reverse()              # 反转得到正确的欧拉回路
    return circuit

# 运行算法，获取欧拉回路顶点序列
euler_vertices = hierholzer(adj)
# 生成边列表（按顺序）
euler_edges = [(euler_vertices[i], euler_vertices[i+1]) for i in range(len(euler_vertices)-1)]
total_edges = len(euler_edges)

print(f"欧拉回路顶点序列: {euler_vertices}")
print(f"共 {total_edges} 条边。")

# ---------- 4. 动画绘制 ----------
fig, ax = plt.subplots(figsize=(8, 6))

def draw_frame(frame):
    """每一帧：绘制前 frame+1 条边，并显示顺序编号"""
    ax.clear()
    # 绘制所有节点
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos, ax=ax)
    # 绘制所有背景边（灰色半透明）
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', alpha=0.3)
    
    # 绘制已选中的欧拉回路边（红色）
    current_edges = euler_edges[:frame+1]
    if current_edges:
        nx.draw_networkx_edges(G, pos, edgelist=current_edges, ax=ax,
                               edge_color='red', width=2.5, connectionstyle='arc3,rad=0.1')
        # 标注边的访问顺序
        for i, (u, v) in enumerate(current_edges):
            x = (pos[u][0] + pos[v][0]) / 2
            y = (pos[u][1] + pos[v][1]) / 2
            ax.text(x, y, str(i+1), fontsize=10, color='darkred',
                    weight='bold', backgroundcolor='white',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    ax.set_title(f"欧拉回路 - 全链路压力测试 (已绘制 {len(current_edges)}/{total_edges} 条边)", fontsize=12)
    ax.axis('off')

# 创建动画，总帧数 = 边数
ani = animation.FuncAnimation(fig, draw_frame, frames=total_edges,
                              interval=1000, repeat=False)   # 间隔1000ms = 1秒

plt.show()