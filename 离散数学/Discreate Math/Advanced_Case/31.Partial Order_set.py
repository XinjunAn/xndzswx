#------------------------------------------------------------------------
# 模拟基于偏序的定时投入关联网络作业调度
#------------------------------------------------------------------------

import heapq
from collections import deque

class Job:
    """网络作业类"""
    def __init__(self, id, duration, deps=None, submit_time=0):
        self.id = id                # 作业唯一标识
        self.duration = duration    # 执行时长
        self.deps = deps if deps else []  # 依赖的作业id列表
        self.submit_time = submit_time    # 可投入时间
        self.rank = None            # 阶位值（最长依赖路径长度）
        self.start_time = None
        self.end_time = None
        self.done = False

    def __repr__(self):
        return f"Job({self.id})"

def compute_ranks(jobs):
    """计算每个作业的阶位值（最长路径长度），基于依赖图 DAG"""
    # 构建邻接表与入度
    adj = {j.id: [] for j in jobs}
    indeg = {j.id: 0 for j in jobs}
    for job in jobs:
        for dep in job.deps:
            adj[dep].append(job.id)
            indeg[job.id] += 1

    # 拓扑排序（Kahn算法），同时更新阶位值（rank）
    q = deque([j.id for j in jobs if indeg[j.id] == 0])
    rank = {j.id: 0 for j in jobs}
    topo_order = []
    while q:
        u = q.popleft()
        topo_order.append(u)
        for v in adj[u]:
            rank[v] = max(rank[v], rank[u] + 1)  # 取最长路径
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(topo_order) != len(jobs):
        raise ValueError("依赖图中存在环，无法计算阶位值。")

    for job in jobs:
        job.rank = rank[job.id]
    return jobs

def simulate_scheduling(jobs):
    """
    模拟单CPU调度，考虑依赖关系和提交时间，按阶位值小优先执行。
    返回作业列表（已填充开始/结束时间）和总完成时间。
    """
    # 计算阶位值
    compute_ranks(jobs)
    job_dict = {j.id: j for j in jobs}
    completed = set()           # 已完成作业id集合
    current_time = 0
    ready_heap = []             # 优先队列 (rank, id)
    # 记录每个作业的依赖完成情况
    remaining_deps = {j.id: set(j.deps) for j in jobs}

    # 初始就绪：无依赖且已到达提交时间的作业
    for job in jobs:
        if not job.deps and job.submit_time <= current_time:
            heapq.heappush(ready_heap, (job.rank, job.id))

    while len(completed) < len(jobs):
        # 若就绪队列为空，推进时间到下一个可提交作业的时间
        if not ready_heap:
            next_time = min(j.submit_time for j in jobs if j.id not in completed)
            current_time = max(current_time, next_time)
            # 检查新到时间的作业，若依赖已完则加入就绪
            for job in jobs:
                if (job.id not in completed and job.submit_time <= current_time
                        and all(dep in completed for dep in job.deps)):
                    heapq.heappush(ready_heap, (job.rank, job.id))
            continue

        # 取出优先级最高的作业
        rank, jid = heapq.heappop(ready_heap)
        job = job_dict[jid]
        if job.id in completed or not all(dep in completed for dep in job.deps):
            continue  # 防御性检查

        # 执行作业
        start = max(current_time, job.submit_time)
        job.start_time = start
        job.end_time = start + job.duration
        current_time = job.end_time
        job.done = True
        completed.add(job.id)
        print(f"执行 {job.id}  | 开始 {job.start_time:>5} | 结束 {job.end_time:>5} | 阶位值 {job.rank}")

        # 解锁依赖本作业的其它作业
        for other in jobs:
            if other.id not in completed and other.submit_time <= current_time:
                if all(dep in completed for dep in other.deps):
                    heapq.heappush(ready_heap, (other.rank, other.id))

    makespan = max(job.end_time for job in jobs)
    return jobs, makespan

# -------------------- 测试案例 --------------------
def run_test(name, jobs):
    print(f"\n========== {name} ==========")
    scheduled_jobs, makespan = simulate_scheduling(jobs)
    print("\n调度结果详情（按开始时间排序）：")
    for job in sorted(scheduled_jobs, key=lambda j: j.start_time):
        print(f"  {job.id}: 开始 {job.start_time:>5}  结束 {job.end_time:>5}  依赖 {job.deps}  阶位值 {job.rank}")
    print(f"总完成时间 (makespan): {makespan}\n")

if __name__ == "__main__":
    # 案例1：基础依赖链（无提交时间差异）
    jobs1 = [
        Job('A', 3, []),
        Job('B', 2, ['A']),
        Job('C', 4, ['A']),
        Job('D', 1, ['B', 'C']),
    ]
    run_test("案例1：基础依赖关系", jobs1)

    # 案例2：不同提交时间（定时投入）
    jobs2 = [
        Job('A', 3, [], submit_time=0),
        Job('B', 2, ['A'], submit_time=5),
        Job('C', 4, ['A'], submit_time=1),
        Job('D', 1, ['B', 'C'], submit_time=2),
        Job('E', 2, [], submit_time=0),  # 独立作业
    ]
    run_test("案例2：不同提交时间", jobs2)

    # 案例3：复杂分支合并
    jobs3 = [
        Job('W', 2, []),
        Job('X', 3, ['W']),
        Job('Y', 1, ['X']),
        Job('Z', 2, ['Y']),
        Job('P', 4, ['W']),
        Job('Q', 2, ['P', 'Z']),
    ]
    run_test("案例3：复杂依赖结构", jobs3)