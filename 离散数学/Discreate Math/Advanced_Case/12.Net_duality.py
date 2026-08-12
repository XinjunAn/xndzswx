#----------------------------------------------
# 云服务器的“隐藏标价”——资源分配的对偶理论
#----------------------------------------------

import numpy as np
from scipy.optimize import linprog
import pandas as pd

# ==============================
# 1. 场景建模
# ==============================
services = ['Web服务', 'AI推理', '数据分析', '视频转码']
resources = ['CPU(核)', '内存(GB)', 'GPU(卡)']

# 每个服务单实例的资源消耗矩阵 A (资源 x 服务)
A = np.array([
    [2,  8,  4,  6],   # CPU
    [4, 16, 32, 12],   # 内存
    [0,  1,  0,  1],   # GPU
])

# 每个服务单实例的收益（元/小时）
c = np.array([10, 80, 40, 30])

# 资源总量（预算约束）
b = np.array([200, 800, 20])  # CPU核, 内存GB, GPU卡

# ==============================
# 2. 求解原问题 (Primal): 收益最大化
# ==============================
# linprog 默认求 min，因此对 c 取负
res_primal = linprog(
    c=-c, A_ub=A, b_ub=b,
    bounds=[(0, None)] * len(services),
    method='highs'
)

x_opt = res_primal.x
max_revenue = -res_primal.fun

print("=" * 60)
print("【原问题 Primal】开发视角：如何部署服务最大化收益？")
print("=" * 60)
df_primal = pd.DataFrame({
    '服务': services,
    '部署实例数': np.round(x_opt, 2),
    '单价(元/h)': c,
    '贡献收益': np.round(x_opt * c, 2),
})
print(df_primal.to_string(index=False))
print(f"\n>>> 最大总收益: {max_revenue:.2f} 元/小时")

# ==============================
# 3. 求解对偶问题 (Dual): 资源影子价格
# ==============================
# Dual: min b^T y  s.t.  A^T y >= c, y >= 0
res_dual = linprog(
    c=b, A_ub=-A.T, b_ub=-c,
    bounds=[(0, None)] * len(resources),
    method='highs'
)

y_opt = res_dual.x
min_cost = res_dual.fun

print("\n" + "=" * 60)
print("【对偶问题 Dual】运维/CFO视角：资源的隐藏标价是多少？")
print("=" * 60)
df_dual = pd.DataFrame({
    '资源': resources,
    '总量': b,
    '影子价格(元/单位)': np.round(y_opt, 4),
    '资源总估值': np.round(b * y_opt, 2),
})
print(df_dual.to_string(index=False))
print(f"\n>>> 最小资源总估值: {min_cost:.2f} 元/小时")

# ==============================
# 4. 强对偶验证 & 经济学解读
# ==============================
print("\n" + "=" * 60)
print("【强对偶定理验证】Primal最优 == Dual最优")
print("=" * 60)
print(f"Primal 最大收益 = {max_revenue:.4f}")
print(f"Dual   最小估值 = {min_cost:.4f}")
print(f"差距 (Duality Gap) = {abs(max_revenue - min_cost):.2e}")

# ==============================
# 5. 互补松弛性 —— 揭示"瓶颈资源"
# ==============================
print("\n" + "=" * 60)
print("【互补松弛性】识别瓶颈资源与非饱和资源")
print("=" * 60)
slack = b - A @ x_opt
for i, r in enumerate(resources):
    status = "🔴 瓶颈(已用满)" if slack[i] < 1e-6 else "🟢 有富余"
    print(f"{r:10s} | 剩余={slack[i]:7.2f} | 影子价={y_opt[i]:.4f} | {status}")

print("\n💡 解读：影子价格 > 0 的资源即为瓶颈；")
print("    每增加 1 单位该资源，总收益可提升 (影子价) 元/小时。")
print("    这就是采购扩容决策的量化依据！")