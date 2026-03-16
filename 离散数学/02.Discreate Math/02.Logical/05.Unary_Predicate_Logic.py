#谓词逻辑案例——云计算集群的“看门狗”协议
import matplotlib.pyplot as plt
import numpy as np

def auto_scaling_audit():
    # 1. 模拟数据生成
    # 生成 50 台服务器的数据
    np.random.seed(42) # 固定随机种子方便教学重现
    num_servers = 50
    
    # x轴: CPU 负载 (0% - 100%)
    cpu_loads = np.random.randint(0, 100, num_servers)
    
    # y轴: 报警状态 (0:未触发, 1:触发)
    # 我们故意制造一些混乱的数据
    alert_status = []
    
    threshold = 80 # P(x) 的阈值
    
    for load in cpu_loads:
        if load > threshold:
            # 高负载时，大部分应该报警(T->T)，但偶发故障不报警(T->F)
            status = 1 if np.random.random() > 0.2 else 0 
        else:
            # 低负载时，大部分不报警(F->F)，但偶发误报(F->T)
            status = 0 if np.random.random() > 0.1 else 1
        alert_status.append(status)

    # 2. 逻辑判断核心代码
    colors = []
    sizes = []
    labels = []
    
    violation_count = 0
    
    for i in range(num_servers):
        p = cpu_loads[i] > threshold  # P(x): 是否高负载
        q = bool(alert_status[i])     # Q(x): 是否报警
        
        # 蕴含式 P -> Q 等价于 (not P) or Q
        is_compliant = (not p) or q
        
        if is_compliant:
            if not p:
                # F -> T/F (空真情况)
                colors.append('lightgreen') # 正常静默或误报
                labels.append('Idle')
            else:
                # T -> T (正常触发)
                colors.append('green')
                labels.append('Active Scale')
            sizes.append(50)
        else:
            # T -> F (故障！！)
            # 这是我们要找的违反全称量词的反例
            colors.append('red') 
            labels.append('FAILURE')
            sizes.append(150) # 放大显示故障点
            violation_count += 1

    # 3. 可视化绘图
    plt.figure(figsize=(12, 6))
    
    # 绘制阈值线
    plt.axvline(x=threshold, color='gray', linestyle='--', label=f'Threshold P(x): CPU > {threshold}%')
    
    # 绘制散点
    # 为了防止点重叠看不清，给Y轴加一点点抖动(Jitter)
    y_jitter = np.array(alert_status) + np.random.normal(0, 0.05, num_servers)
    
    plt.scatter(cpu_loads, y_jitter, c=colors, s=sizes, alpha=0.7, edgecolors='black')

    # 添加区域注解
    # 右下角区域 (High CPU, No Alert) -> 死亡区域
    plt.fill_betweenx([-0.2, 0.5], threshold, 105, color='salmon', alpha=0.2)
    plt.text(90, 0.25, "VIOLATION ZONE\n(T -> F)", color='red', ha='center', fontweight='bold')

    # 右上角区域 (High CPU, Alert On) -> 正常工作
    plt.text(90, 0.9, "Working\n(T -> T)", color='green', ha='center')
    
    # 左侧区域 (Low CPU) -> 空真
    plt.text(40, 0.5, "Vacuous Truth Zone\n(P is False -> Always True)\nSystem Idle or False Alarm", 
             color='gray', ha='center', fontsize=12)

    # 设置图表属性
    plt.title(f"Cluster Logic Audit: ∀x (HighLoad(x) -> Alert(x))\nViolations Found: {violation_count}", fontsize=14)
    plt.xlabel("CPU Load (%) - Predicate P(x)")
    plt.ylabel("Alert Triggered (1=Yes, 0=No) - Predicate Q(x)")
    plt.yticks([0, 1], ['OFF', 'ON'])
    plt.xlim(0, 105)
    plt.ylim(-0.3, 1.3)
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    auto_scaling_audit()