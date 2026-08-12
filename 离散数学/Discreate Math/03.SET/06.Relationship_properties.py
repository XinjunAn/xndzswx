#------------------------------------------------------------------
# 判断A集合上的任意关系R，通过判断其自反、对称、可传递特性来判断关系的性质
# 包括其是否是等价关系、相容关系、偏序关系
#------------------------------------------------------------------
import random

# ------------------------- 性质判断函数 -------------------------


# 判断自反性: 所有 x∈A，都有 (x,x)∈R
def Is_reflexive(A, R):
    for x in A:
        if (x, x) not in R:
            return False
    return True
# 判断对称性: 若 (x,y)∈R 则 (y,x)∈R
def Is_symmetric(R):
    for (x, y) in R:
        if (y, x) not in R:
            return False
    return True
# 判断反对称性: 若 (x,y)∈R 且 (y,x)∈R，则 x == y
def Is_antisymmetric(R):
    for (x, y) in R:
        if (y, x) in R and x != y:
            return False
    return True
# 判断传递性: 若 (x,y)∈R 且 (y,z)∈R，则 (x,z)∈R
def Is_transitive(R):
    # 将关系转为列表以便多重遍历
    rel_list = list(R)
    for (x, y) in rel_list:
        for (a, b) in rel_list:
            # 如果前一个的y等于后一个的x，检查传递对是否存在
            if y == a:
                if (x, b) not in R:
                    return False
    return True

# ------------------------- 主逻辑 -------------------------

def main():
    print("=" * 50)
    print("二元关系性质自动判断器（随机生成）")
    print("=" * 50)
    
    # 1. 终端输入
    try:
        n = int(input("请输入集合A的元素个数,输入正整数 (例如 3): "))
        m = int(input("请输入要生成的序偶个数 ，正整数且不超过A元素的平方值(例如 4): "))
        if n <= 0 or m < 0:
            print("错误：元素个数必须大于0，序偶个数不能为负数。")
            return
    except ValueError:
        print("错误：请输入有效的整数。")
        return

    # 2. 生成集合A (用数字 1,2,...,n 表示元素)
    A = list(range(1, n + 1))
    max_pairs = n * n
    
    if m > max_pairs:
        print(f"⚠️ 警告：集合A上最多只有 {max_pairs} 个不同的序偶，已自动调整为最大值。")
        m = max_pairs

    # 随机生成 m 个不同的序偶 (使用set保证唯一性)
    R = set()
    # 若m接近最大值，随机抽取可能很慢，这里直接生成全部组合再随机抽样
    if m == max_pairs:
        # 生成笛卡尔积全集
        for x in A:
            for y in A:
                R.add((x, y))
    else:
        # 普通情况：暴力随机直到凑够m个
        attempts = 0
        while len(R) < m and attempts < 100000:  # 防止死循环
            x = random.choice(A)
            y = random.choice(A)
            R.add((x, y))
            attempts += 1
        # 万一随机不到那么多（概率极低），补全剩余的用顺序生成补丁
        if len(R) < m:
            print("⚠️ 随机生成较慢，切换为顺序补全模式...")
            for x in A:
                for y in A:
                    if len(R) >= m:
                        break
                    R.add((x, y))
                if len(R) >= m:
                    break

    # 3. 判断各项性质
    ref = Is_reflexive(A, R)
    sym = Is_symmetric(R)
    antisym = Is_antisymmetric(R)
    trans = Is_transitive(R)

    # 4. 输出原始数据
    print("\n" + "-" * 50)
    print(f"集合 A = {A}")
    print(f"关系 R = {sorted(list(R))}")  # 排序后打印更清晰
    print("-" * 50)
    
    # 5. 打印性质明细
    print("【性质检查结果】")
    print(f"  自反性 (Reflexive)    : {ref}")
    print(f"  对称性 (Symmetric)    : {sym}")
    print(f"  反对称性 (Antisymmetric): {antisym}")
    print(f"  传递性 (Transitive)   : {trans}")
    print("-" * 50)

    # 6. 综合判断关系类型 (按数学优先级: 等价 > 相容 > 偏序)
    if ref and sym and trans:
        print("✅ 判定结果：该关系是 【等价关系】 (同时也满足相容关系)")
    elif ref and sym:
        print("✅ 判定结果：该关系是 【相容关系】 (满足自反+对称，但不具有传递性)")
    elif ref and antisym and trans:
        print("✅ 判定结果：该关系是 【偏序关系】")
    else:
        print("❌ 判定结果：该关系是 【普通二元关系】，不属于以上三种特殊关系")
    
    print("=" * 50)

if __name__ == "__main__":
    main()