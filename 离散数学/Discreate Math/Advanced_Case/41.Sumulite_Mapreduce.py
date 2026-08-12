from typing import TypeVar, Generic, Callable, List
from functools import reduce
from concurrent.futures import ThreadPoolExecutor
import random

A = TypeVar('A')


class Monoid(Generic[A]):
    """幺半群抽象：单位元 + 结合二元运算"""
    def __init__(self, empty: A, combine: Callable[[A, A], A]):
        self.empty = empty
        self.combine = combine

    def concat(self, items: List[A]) -> A:
        """对列表执行 fold（归约），空列表返回单位元"""
        return reduce(self.combine, items, self.empty)


# ============ 预定义常用幺半群 ============

# 整数加法幺半群：单位元0，运算+
monoid_sum = Monoid[int](0, lambda a, b: a + b)

# 整数最大值幺半群：单位元负无穷，运算max
monoid_max = Monoid[int](float('-inf'), lambda a, b: max(a, b))

# 字符串拼接幺半群：单位元空串，运算+
monoid_str_concat = Monoid[str]("", lambda a, b: a + b)

# 列表拼接幺半群：单位元空列表，运算extend
monoid_list_concat = Monoid[List]([], lambda a, b: a + b)


# ============ 模拟 MapReduce 并行聚合 ============

def parallel_aggregate(monoid: Monoid[A], data: List[A], num_workers: int = 4) -> A:
    """
    模拟 MapReduce 并行聚合：
    1. 将数据分片
    2. 各 worker 并行计算局部聚合
    3. 合并各 worker 的结果（顺序任意，结果一致）
    """
    if not data:
        return monoid.empty

    # 1. 数据分片
    chunk_size = max(1, len(data) // num_workers)
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # 2. 并行计算各分片（模拟多线程）
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # 每个 worker 对分片执行 concat
        futures = [executor.submit(monoid.concat, chunk) for chunk in chunks]
        partial_results = [f.result() for f in futures]

    # 3. 合并各 worker 结果（任意顺序，依赖结合律保证一致性）
    return monoid.concat(partial_results)


# ============ 运行演示 ============
if __name__ == "__main__":
    # 生成 10000 个随机整数
    data = [random.randint(1, 100) for _ in range(10000)]

    print(f"数据集大小: {len(data)}")
    print(f"前10个数据: {data[:10]}...\n")

    # 使用加法幺半群求和（并行）
    result_sum = parallel_aggregate(monoid_sum, data, num_workers=4)
    print(f"并行求和结果: {result_sum}")
    print(f"串行求和验证: {sum(data)}")
    print(f"结果一致: {result_sum == sum(data)}\n")

    # 使用最大值幺半群求最大值（并行）
    result_max = parallel_aggregate(monoid_max, data, num_workers=4)
    print(f"并行求最大值结果: {result_max}")
    print(f"串行求最大值验证: {max(data)}")
    print(f"结果一致: {result_max == max(data)}\n")

    # 字符串拼接（演示任意顺序合并的一致性）
    words = ["Hello", " ", "World", "!", " ", "Monoid", " ", "is", " ", "powerful"]
    result_str = parallel_aggregate(monoid_str_concat, words, num_workers=3)
    print(f"并行字符串拼接: '{result_str}'")