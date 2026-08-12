#----------------------------------------------------------------------
# CRDT（Conflict-free Replicated Data Type，无冲突复制数据类型）
# 让多个副本自动收敛到一致状态的数据结构
#----------------------------------------------------------------------
from dataclasses import dataclass
from typing import List


# 定义增长计数器类，含2个属性，3个操作分别是增长、合并、取值操作
class GCounter:
    """增长计数器 CRDT——每个副本维护一个向量，分量代表各节点的计数值"""
    node_id: int          # 当前节点ID
    counts: List[int]     # counts[i] = 节点i的计数值

    def __post_init__(self):
        # 确保每个节点至少有一个槽位
        if self.node_id >= len(self.counts):
            self.counts.extend([0] * (self.node_id - len(self.counts) + 1))

    def increment(self) -> 'GCounter':
        """当前节点计数+1"""
        new_counts = self.counts.copy()
        new_counts[self.node_id] += 1
        return GCounter(self.node_id, new_counts)

    def value(self) -> int:
        """获取当前总值"""
        return sum(self.counts)

    def merge(self, other: 'GCounter') -> 'GCounter':
        """
        合并两个计数器——取各分量最大值。
        这是一个交换半群运算：
        - 结合律：merge(merge(a,b), c) == merge(a, merge(b,c))
        - 交换律：merge(a,b) == merge(b,a)
        """
        max_len = max(len(self.counts), len(other.counts))
        new_counts = [
            max(
                self.counts[i] if i < len(self.counts) else 0,
                other.counts[i] if i < len(other.counts) else 0
            )
            for i in range(max_len)
        ]
        return GCounter(self.node_id, new_counts)


# ============ 运行演示 ============
if __name__ == "__main__":
    # 三个节点各自初始化
    node_a = GCounter(0, [0, 0, 0])
    node_b = GCounter(1, [0, 0, 0])
    node_c = GCounter(2, [0, 0, 0])

    # 各节点独立操作（无锁并发）
    a_updated = node_a.increment().increment()   # A节点执行了2次增量
    b_updated = node_b.increment()                # B节点执行了1次增量
    c_updated = node_c.increment().increment().increment()  # C节点执行了3次增量

    print(f"A节点状态: {a_updated.counts}, 总值={a_updated.value()}")
    print(f"B节点状态: {b_updated.counts}, 总值={b_updated.value()}")
    print(f"C节点状态: {c_updated.counts}, 总值={c_updated.value()}")

    # 模拟网络同步：任意顺序合并，结果一致
    # 顺序1: A合并B，再合并C
    merged_1 = a_updated.merge(b_updated).merge(c_updated)
    # 顺序2: B合并C，再合并A
    merged_2 = b_updated.merge(c_updated).merge(a_updated)

    print(f"\n合并结果1 (A←B←C): {merged_1.counts}, 总值={merged_1.value()}")
    print(f"合并结果2 (B←C←A): {merged_2.counts}, 总值={merged_2.value()}")
    print(f"两种合并顺序结果一致: {merged_1.counts == merged_2.counts}")