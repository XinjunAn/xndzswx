class UnionFind:
    """并查集，支持任意可哈希对象作为顶点（例如字符串）"""
    def __init__(self, vertices):
        # 每个顶点的父节点初始化为自身
        self.parent = {v: v for v in vertices}
        # 秩（树的高度上界）初始化为 0
        self.rank = {v: 0 for v in vertices}

    def find(self, x):
        """查找 x 的根节点，同时进行路径压缩"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """
        合并 x 和 y 所在的集合，按秩合并
        返回 True 表示合并成功，False 表示已在同一集合（会形成环）
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False

        # 将秩小的树合并到秩大的树上
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True


def kruskal(edges):
    """
    Kruskal 算法求最小生成树
    :param edges: 边的列表，每条边为 (顶点u, 顶点v, 权重w)
    :return: (mst_edges, total_weight)
    """
    # 1. 从边列表中提取所有不重复的顶点
    vertices = set()
    for u, v, w in edges:
        vertices.add(u)
        vertices.add(v)

    # 2. 按权重升序排序边
    sorted_edges = sorted(edges, key=lambda e: e[2])

    # 3. 初始化并查集
    uf = UnionFind(vertices)

    mst = []          # 存放最小生成树的边
    total_weight = 0  # 最小生成树的总权值
    V = len(vertices) # 顶点总数

    # 4. 遍历排序后的边，贪心选择
    for u, v, w in sorted_edges:
        if uf.union(u, v):          # 若 u 和 v 不连通，则加入该边
            mst.append((u, v, w))
            total_weight += w
            # 当已选边数 = V-1 时，生成树完成，可提前结束
            if len(mst) == V - 1:
                break

    # 5. 连通性检查
    if len(mst) < V - 1:
        print("警告：图不连通，无法生成完整的最小生成树！")

    return mst, total_weight


if __name__ == "__main__":
    # 定义图的边，顶点用字母表示，权重为整数
    edges1 = [
        ('a', 'b', 6),
        ('a', 'c', 7),
        ('b', 'c', 2),
        ('b', 'd', 8),
        ('c', 'd', 5),
        ('c', 'e', 4),
        ('d', 'e', 1),
        ('d', 'f', 3),
        ('d', 'e', 5),
        ('e', 'f', 5),
        ('f', 'g', 4)
    ]
    edges2 = [
        ('a', 'b', 2),
        ('a', 'g', 2),
        ('a', 'f', 7),
        ('b', 'c', 4),
        ('b', 'g', 5),
        ('g', 'f', 5),
        ('g', 'c', 1),
        ('g', 'd', 3),
        ('c', 'd', 4),
        ('e', 'f', 5),
        ('f', 'd', 1),
        ('e', 'd', 7)
        
    ]

    mst1, total1 = kruskal(edges1)
    mst2, total2 = kruskal(edges2)
    

    print("第一个图的最小生成树的边：")
    for u, v, w in mst1:
        print(f"  {u} -- {v}  权值: {w}")
    print(f"总权值: {total1}")
    print("第二个图的最小生成树的边：")
    for u, v, w in mst2:
        print(f"  {u} -- {v}  权值: {w}")
    print(f"总权值: {total2}")