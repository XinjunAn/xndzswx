#半群理论的应用案例——Git 的版本合并与“半群”特性
import time
import functools
from multiprocessing import Pool

# === 1. 定义幺半群 (Monoid) ===
# 一个幺半群需要:
#   1. 集合 (这里是整数)
#   2. 运算 (这里是加法 combine)
#   3. 单位元 (这里是 0)

def combine(a, b):
    # 模拟一个稍微耗时的运算，代表服务器处理日志
    # time.sleep(0.001) 
    return a + b

identity_element = 0

# === 2. 模拟分布式计算场景 ===

def process_chunk(chunk):
    """
    模拟一台服务器处理一部分数据。
    它在内部利用半群的性质进行局部聚合 (Local Reduce)。
    """
    # 使用 functools.reduce 进行折叠运算
    # reduce(fn, [a, b, c, d]) essentially does ((a+b)+c)+d
    return functools.reduce(combine, chunk, identity_element)

def teach_monoid_mapreduce():
    # 假设我们有海量数据需要汇总
    data = list(range(1, 101)) # 1 到 100
    
    print(f"原始数据: {data[:10]} ... {data[-10:]}")
    print(f"数据总量: {len(data)}")
    
    # === 方案 A: 顺序计算 (单机模式) ===
    # ((1+2)+3)+4... 严格的线性结合
    start_time = time.time()
    result_sequential = functools.reduce(combine, data, identity_element)
    print(f"\n[单机模式] 结果: {result_sequential}")
    
    # === 方案 B: 分布式并行计算 (MapReduce) ===
    # 利用半群的结合律: (1+2+3) + (4+5+6) + (7+8+9) ...
    # 我们可以随意切分数据，并行计算括号里的内容，最后再把括号的结果加起来
    
    # 将数据切成 4 份 (Sharding)
    num_chunks = 4
    chunk_size = len(data) // num_chunks
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    print(f"\n[分布式模式] 将数据切分为 {len(chunks)} 个分片，准备并行计算...")
    
    # 并行处理 (Map 阶段)
    # 这里用简单的列表推导模拟多台机器同时工作
    partial_results = [process_chunk(chk) for chk in chunks]
    print(f"  -> 各分片局部汇总结果: {partial_results}")
    
    # 全局汇总 (Reduce 阶段)
    # 将各分片的结果再进行一次半群运算
    final_result_distributed = functools.reduce(combine, partial_results, identity_element)
    
    print(f"  -> 最终汇总结果: {final_result_distributed}")
    
    # === 验证 ===
    # 结合律保证了：无论怎么切分、怎么分组，结果必须一致
    if result_sequential == final_result_distributed:
        print("\n✅ 验证成功！结合律成立 (Associativity holds).")
        print("   (a + b) + c == a + (b + c)")
    else:
        print("\n❌ 验证失败！")

if __name__ == "__main__":
    teach_monoid_mapreduce()