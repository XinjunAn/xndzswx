#软件设计中的“权限控制电路” (逻辑门模拟)
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def simulate_auth_logic(has_key, password_correct, super_mode):
    # 1. 计算逻辑结果
    # 逻辑: Key ∧ (Password ∨ SuperMode)
    logic_or_result = password_correct or super_mode
    final_launch_ready = has_key and logic_or_result
    
    # 2. 设置绘图画布
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    plt.title("Software Logic Gate Simulator: Key ∧ (Pwd ∨ Super)", fontsize=14)

    # 3. 绘制逻辑门连线函数 (辅助绘图)
    def draw_box(x, y, text, color='lightgray', width=1.5):
        rect = patches.Rectangle((x, y), width, 1, linewidth=2, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        ax.text(x + width/2, y + 0.5, text, ha='center', va='center', fontsize=10, fontweight='bold')

    def draw_line(x1, y1, x2, y2, active):
        color = '#32CD32' if active else '#FF4500' # 亮绿 或 红
        style = '-' if active else '--'
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=3, linestyle=style)

    # === 绘制输入端 (Inputs) ===
    draw_box(0.5, 4.5, f"Physical Key\n{has_key}", color='#87CEEB' if has_key else 'lightgray')
    draw_box(0.5, 2.5, f"Password\n{password_correct}", color='#87CEEB' if password_correct else 'lightgray')
    draw_box(0.5, 0.5, f"Super Mode\n{super_mode}", color='#87CEEB' if super_mode else 'lightgray')

    # === 第一层逻辑：OR 门 (Pwd ∨ Super) ===
    # 模拟电路位置
    or_gate_x, or_gate_y = 4, 1.5
    draw_box(or_gate_x, or_gate_y, "OR Gate\n(∨)", color='white')
    
    # 连线: Password -> OR
    draw_line(2, 3, 4, 2.2, password_correct)
    # 连线: Super -> OR
    draw_line(2, 1, 4, 1.8, super_mode)
    
    # === 第二层逻辑：AND 门 (Key ∧ OR_Result) ===
    and_gate_x, and_gate_y = 7, 3
    draw_box(and_gate_x, and_gate_y, "AND Gate\n(∧)", color='white')
    
    # 连线: Key -> AND
    draw_line(2, 5, 7, 3.8, has_key)
    # 连线: OR结果 -> AND
    draw_line(5.5, 2, 7, 3.2, logic_or_result)

    # === 输出端 (Output) ===
    final_color = '#00FF00' if final_launch_ready else '#555555' # 亮绿 或 暗灰
    circle = patches.Circle((9.5, 3.5), 0.4, linewidth=2, edgecolor='black', facecolor=final_color)
    ax.add_patch(circle)
    ax.text(9.5, 2.8, "LAUNCH", ha='center', fontweight='bold')

    plt.show()

# === 教学演示：修改参数体验逻辑门 ===
# 情况 A: 只有密码，没钥匙 -> 无法发射
print("Simulation A: Password OK, No Key")
simulate_auth_logic(has_key=False, password_correct=True, super_mode=False)

# 情况 B: 有钥匙，忘了密码，但是是超级管理员 -> 可以发射
# print("Simulation B: Key OK, Super Mode Override")
# simulate_auth_logic(has_key=True, password_correct=False, super_mode=True)