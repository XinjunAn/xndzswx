import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from collections import defaultdict

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 构建图（完全图K5）
n = 5
adj = {i: [j for j in range(n) if j != i] for i in range(n)}
G = nx.complete_graph(n)
pos = nx.spring_layout(G, seed=42)  # 固定布局

# 欧拉回路算法（Hierholzer）
def hierholzer(adj):
    graph = {u: adj[u][:] for u in adj}
    for v in graph:
        if len(graph[v]) % 2 != 0:
            raise ValueError("Not Eulerian")
    stack = []
    circuit = []
    start = 0
    curr = start
    stack.append(curr)
    while stack:
        if graph[curr]:
            stack.append(curr)
            nxt = graph[curr].pop()
            graph[nxt].remove(curr)
            curr = nxt
        else:
            circuit.append(curr)
            curr = stack.pop()
    circuit.reverse()
    return circuit

euler_vertices = hierholzer(adj)
euler_edges = [(euler_vertices[i], euler_vertices[i+1]) for i in range(len(euler_vertices)-1)]

# 哈密尔顿回路算法（回溯）
def hamiltonian_cycle(adj, n):
    path = []
    visited = [False]*n
    def dfs(curr, depth):
        path.append(curr)
        if depth == n:
            if path[0] in adj[curr]:
                return True
            else:
                path.pop()
                return False
        visited[curr] = True
        for nxt in adj[curr]:
            if not visited[nxt]:
                if dfs(nxt, depth+1):
                    return True
        visited[curr] = False
        path.pop()
        return False
    if dfs(0,1):
        return path + [path[0]]
    return None

ham_vertices = hamiltonian_cycle(adj, n)
ham_edges = [(ham_vertices[i], ham_vertices[i+1]) for i in range(len(ham_vertices)-1)]

# 设置动画
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 预先绘制静态元素（节点、背景边）
def draw_graph(ax, edges_highlight, edge_labels, title):
    ax.clear()
    # 绘制所有节点
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos, ax=ax)
    # 绘制背景边（灰色）
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', alpha=0.3)
    # 绘制高亮边
    if edges_highlight:
        nx.draw_networkx_edges(G, pos, edgelist=edges_highlight, ax=ax,
                               edge_color='red' if title.startswith('欧拉') else 'blue',
                               width=2.5, connectionstyle='arc3,rad=0.1')
    # 绘制顺序标签
    for i, (u,v) in enumerate(edges_highlight):
        x = (pos[u][0]+pos[v][0])/2
        y = (pos[u][1]+pos[v][1])/2
        ax.text(x, y, str(i+1), fontsize=9, color='darkred' if title.startswith('欧拉') else 'darkblue',
                weight='bold', backgroundcolor='white', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax.set_title(title, fontsize=12)
    ax.axis('off')

# 动画更新函数
def update(frame):
    # frame从0到总边数-1，每帧增加一条边
    # 欧拉边数
    euler_len = len(euler_edges)
    ham_len = len(ham_edges)
    # 同时显示两边，按各自的顺序
    euler_show = euler_edges[:min(frame+1, euler_len)]
    ham_show = ham_edges[:min(frame+1, ham_len)]
    draw_graph(ax1, euler_show, [], "欧拉回路（全链路压力测试）")
    draw_graph(ax2, ham_show, [], "哈密尔顿回路（令牌环/数据采集）")
    # 返回绘制的对象（略）
    return ax1, ax2

# 总帧数为两者最大边长
total_frames = max(len(euler_edges), len(ham_edges))
ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=1000, repeat=False)

plt.show()