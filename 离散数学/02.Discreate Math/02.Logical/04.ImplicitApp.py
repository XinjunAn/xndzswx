#数理逻辑案例——API 接口的“契约精神”与自动化测试
import matplotlib.pyplot as plt
import numpy as np

def teach_implication_testing():
    # 模拟用户数据库与权限系统
    # 格式: (用户名, 是否管理员P, 是否有删除权限Q)
    test_users = [
        ("User_A", True,  True),   # 管理员，有权限
        ("User_B", True,  False),  # 管理员，无权限 (BUG!)
        ("User_C", False, False),  # 普通用户，无权限
        ("User_D", False, True)    # 普通用户，有权限 (逻辑上符合 P->Q)
    ]

    # 定义蕴含逻辑函数
    def implication(p, q):
        # Python中没有 -> 运算符，使用等价式: (not P) or Q
        return (not p) or q

    # 准备绘图数据
    results = []
    labels = []
    colors = []
    
    print(f"{'User':<10} | {'IsAdmin(P)':<10} | {'CanDel(Q)':<10} | {'P -> Q Check'}")
    print("-" * 55)

    for user, p, q in test_users:
        is_compliant = implication(p, q)
        results.append(is_compliant)
        
        status_str = "PASS" if is_compliant else "FAIL (Violation)"
        print(f"{user:<10} | {str(p):<10} | {str(q):<10} | {status_str}")
        
        # 记录用于画图的信息
        labels.append(f"{user}\nP={p}\nQ={q}")
        if is_compliant:
            if not p:
                colors.append('#90EE90') # 浅绿 (空真 Vacuous Truth)
            else:
                colors.append('#32CD32') # 深绿 (正常真)
        else:
            colors.append('#FF4500') # 红色 (违约 False)

    # --- 可视化：蕴含式真值矩阵 ---
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 我们在一个 2x2 的矩阵中画出这4个用户的位置
    # X轴: P (Is Admin), Y轴: Q (Can Delete)
    # 为了画图方便，我们手动映射坐标
    # A(T,T), B(T,F), C(F,F), D(F,T)
    coordinates = {
        "User_A": (1, 1),
        "User_B": (1, 0),
        "User_C": (0, 0),
        "User_D": (0, 1)
    }

    # 绘制背景分区
    # 区域 1 (x=0..1, y=0..1): P=False -> 总是 True (绿色背景)
    rect_vacuous = plt.Rectangle((0, 0), 0.5, 1, color='#E0FFE0', alpha=0.5, label='Vacuous Truth zone')
    ax.add_patch(rect_vacuous)

    # 绘制数据点
    for i, (user, p, q) in enumerate(test_users):
        x = 0.75 if p else 0.25
        y = 0.75 if q else 0.25
        
        # 画圆圈代表用户
        circle = plt.Circle((x, y), 0.12, color=colors[i], ec='black')
        ax.add_patch(circle)
        
        # 标注文字
        ax.text(x, y, user, ha='center', va='center', fontweight='bold', color='white' if not results[i] else 'black')
        
        # 标注 P->Q 结果
        res_text = "PASS" if results[i] else "FAIL"
        ax.text(x, y - 0.18, res_text, ha='center', va='center', fontsize=10, fontweight='bold', color=colors[i])

    # 设置坐标轴标签
    ax.set_xticks([0.25, 0.75])
    ax.set_xticklabels(['Not Admin (P=False)', 'Is Admin (P=True)'], fontsize=12)
    ax.set_yticks([0.25, 0.75])
    ax.set_yticklabels(['Cannot Delete (Q=False)', 'Can Delete (Q=True)'], fontsize=12, rotation=90, va='center')
    
    # 标题与装饰
    plt.title("Software Testing: Logic Implication (P -> Q)\nRule: If Admin, Then Can Delete", fontsize=14)
    plt.axvline(x=0.5, color='gray', linestyle='--')
    plt.axhline(y=0.5, color='gray', linestyle='--')
    
    # 添加注解
    plt.text(0.75, 0.05, "The ONLY False Case\n(Broken Promise)", ha='center', color='red', fontsize=10, style='italic')
    plt.text(0.25, 0.5, "Vacuous Truth\n(P is False, Promise kept by default)", ha='center', color='green', alpha=0.6, fontsize=10)

    plt.axis([0, 1, 0, 1])
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    teach_implication_testing()
    
