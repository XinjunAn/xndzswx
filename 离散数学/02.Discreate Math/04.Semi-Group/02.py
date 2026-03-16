import numpy as np
import matplotlib.pyplot as plt

def generate_pattern(shape, style='vertical'):
    """生成模拟数据的辅助函数"""
    data = np.zeros(shape)
    if style == 'vertical':
        for i in range(0, shape[1], 20):
            data[:, i:i+10] = 1 # 竖条纹
    elif style == 'horizontal':
        for i in range(0, shape[0], 20):
            data[i:i+10, :] = 1 # 横条纹
    return data

def teach_raid_xor_group():
    # 图像大小
    height, width = 100, 100
    
    # === Step 1: 准备硬盘数据 (Disk 1 & Disk 2) ===
    # Disk 1: 竖条纹图像 (代表用户数据 A)
    disk1_data = generate_pattern((height, width), 'vertical')
    
    # Disk 2: 横条纹图像 (代表用户数据 B)
    disk2_data = generate_pattern((height, width), 'horizontal')
    
    # === Step 2: 计算校验盘 (Parity Disk) ===
    # 利用群运算: P = D1 ⊕ D2
    # numpy 的 bitwise_xor 对应数学上的 ⊕
    # 注意: 为了演示方便，这里用0/1矩阵，实际是二进制流
    parity_disk = np.bitwise_xor(disk1_data.astype(int), disk2_data.astype(int))
    
    # === Step 3: 模拟灾难 (Disaster Simulation) ===
    # 假设 Disk 2 物理损坏，数据完全丢失 (变成全0或噪声)
    disk2_damaged = np.zeros((height, width)) 
    
    # === Step 4: 数据恢复 (Data Recovery) ===
    # 利用群的逆元性质: D2 = D1 ⊕ P
    # 证明: D1 ⊕ P = D1 ⊕ (D1 ⊕ D2) = (D1 ⊕ D1) ⊕ D2 = 0 ⊕ D2 = D2
    recovered_data = np.bitwise_xor(disk1_data.astype(int), parity_disk)
    
    # === Step 5: 可视化结果 ===
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    
    # 第一行: 正常状态
    axes[0, 0].imshow(disk1_data, cmap='Blues')
    axes[0, 0].set_title("Disk 1 (Data A)")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(disk2_data, cmap='Reds')
    axes[0, 1].set_title("Disk 2 (Data B)")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(parity_disk, cmap='Greens')
    axes[0, 2].set_title("Parity Disk (P = A $\oplus$ B)\n(XOR Group Operation)")
    axes[0, 2].axis('off')
    
    # 第二行: 灾难与恢复
    axes[1, 0].text(0.5, 0.5, "Disk 1 is OK", ha='center')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(disk2_damaged, cmap='gray')
    axes[1, 1].set_title("⚠ Disk 2 FAILED (Lost) ⚠")
    axes[1, 1].axis('off')
    
    # 恢复结果展示
    axes[1, 2].imshow(recovered_data, cmap='Reds')
    axes[1, 2].set_title("Recovered Disk 2\n(Calculated: A $\oplus$ P)")
    axes[1, 2].axis('off')

    plt.suptitle("RAID 5 Data Recovery Demonstration\nUsing Group Theory (XOR)", fontsize=16)
    plt.tight_layout()
    plt.show()
    
    # 验证数据是否完全一致
    is_perfect = np.array_equal(disk2_data, recovered_data)
    print(f"数据恢复一致性检查: {'✅ 完美恢复' if is_perfect else '❌ 失败'}")

if __name__ == "__main__":
    teach_raid_xor_group()
