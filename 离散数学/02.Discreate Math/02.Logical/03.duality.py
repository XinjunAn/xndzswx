#数理逻辑案例——对偶问题在云服务器的“隐藏标价”的问题
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

def teach_lp_duality():
    # === 1. 定义原问题 (Primal Problem) ===
    # 目标：最大化利润 30*x1 + 40*x2
    # scipy.linprog 默认是求最小化，所以目标函数系数取负数
    c = [-30, -40] 
    
    # 约束条件 (CPU 和 内存限制)
    # 2*x1 + 1*x2 <= 16  (CPU 约束)
    # 1*x1 + 3*x2 <= 24  (内存约束)
    A = [[2, 1], 
         [1, 3]]
    b = [16, 24]
    
    # 变量边界：x1, x2 必须 >= 0
    x_bounds = (0, None)
    
    # === 2. 求解问题 ===
    # linprog 使用内点法/单纯形法求解
    res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, x_bounds], method='highs')
    
    # === 3. 提取结果 (原问题与对偶问题) ===
    optimal_x1, optimal_x2 = res.x
    max_profit = -res.fun
    
    # 【核心！】获取对偶问题的解 (影子价格 Shadow Prices)
    # 在 scipy 中，ineqlin 属性包含了不等式约束的对偶变量值（即拉格朗日乘子）
    shadow_price_cpu = res.ineqlin.marginals[0] * -1
    shadow_price_mem = res.ineqlin.marginals[1] * -1

    print("=== 原问题结果 (开发部署方案) ===")
    print(f"最佳部署：Web 服务 = {optimal_x1:.2f} 个, Data 服务 = {optimal_x2:.2f} 个")
    print(f"最大总收益：{max_profit:.2f} 元/小时")
    
    print("\n=== 对偶问题结果 (运维扩容指导 - 影子价格) ===")
    print(f"CPU 的影子价格：{shadow_price_cpu:.2f} 元/核")
    print(f"内存的影子价格：{shadow_price_mem:.2f} 元/GB")
    
    if shadow_price_cpu > shadow_price_mem:
        print("-> 结论：CPU 是更大的瓶颈！优先把预算花在升级 CPU 上。")
    else:
        print("-> 结论：内存是更大的瓶颈！优先把预算花在升级内存上。")

    # === 4. 可视化原问题的可行域 ===
    x = np.linspace(0, 15, 200)
    
    # 计算约束线
    # 2x1 + x2 = 16  => x2 = 16 - 2x1
    y1 = 16 - 2*x
    # x1 + 3x2 = 24  => x2 = (24 - x1) / 3
    y2 = (24 - x) / 3
    
    plt.figure(figsize=(8, 6))
    
    # 绘制约束线
    plt.plot(x, y1, label=r'CPU Limit ($2x_1 + x_2 \leq 16$)', color='red', linewidth=2)
    plt.plot(x, y2, label=r'Memory Limit ($x_1 + 3x_2 \leq 24$)', color='blue', linewidth=2)
    
    # 填充可行域
    y_min = np.minimum(y1, y2)
    plt.fill_between(x, 0, y_min, where=(y_min >= 0) & (x >= 0), color='gray', alpha=0.3, label='Feasible Region')
    
    # 标注最优点
    plt.plot(optimal_x1, optimal_x2, 'g*', markersize=15, label=f'Optimal Point ({optimal_x1:.1f}, {optimal_x2:.1f})')
    
    # 绘制等利润线 (目标函数) 30x1 + 40x2 = max_profit
    y_obj = (max_profit - 30*x) / 40
    plt.plot(x, y_obj, 'g--', label='Objective Function (Max Profit)', linewidth=2)

    # 图表设置
    plt.xlim(0, 12)
    plt.ylim(0, 12)
    plt.xlabel('Number of Web Services ($x_1$)')
    plt.ylabel('Number of Data Services ($x_2$)')
    plt.title(f'Cloud Resource Allocation\nMax Profit: ${max_profit:.1f} | Shadow Prices: CPU=${shadow_price_cpu:.1f}, RAM=${shadow_price_mem:.1f}')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # 在图上添加对偶意义的文字说明
    plt.text(6, 8, f"If you buy 1 more CPU,\nProfit increases by ${shadow_price_cpu:.0f}", bbox=dict(facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    teach_lp_duality()