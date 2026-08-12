#------------------------------------------------------------------
# 随机数构造一个A集合，随机产生一个A集合上的二元关系R，判断是否构成函数
#------------------------------------------------------------------

import random
import itertools
import string

# 1. 获取集合大小
while True:
    try:
        n = int(input("请输入集合 A 的大小（正整数，不超过26）："))
        if 1 <= n <= 26:
            break
        else:
            print("大小必须在 1~26 之间。")
    except ValueError:
        print("请输入一个正整数。")

# 2. 随机生成由 n 个不同小写字母组成的集合 A
all_letters = list(string.ascii_lowercase)   # ['a', 'b', ..., 'z']
letters = random.sample(all_letters, n)      # 随机选取 n 个不同字母
A = sorted(letters)                          # 按字母顺序排列
print("\n集合 A:", A)

# 3. 随机生成一个隐藏的双射 f（排列）
perm_f = A.copy()
random.shuffle(perm_f)
f = {A[i]: perm_f[i] for i in range(n)}
print("隐藏的双射 f:", f)

# 4. 生成二元关系 R（保证包含 f 的所有序偶，再随机混入其他序偶）
R = set()
# 加入 f 的序偶
for x, y in f.items():
    R.add((x, y))

# 以概率 p = 0.3 加入其他序偶
p = 0.3
for x in A:
    for y in A:
        if (x, y) not in R and random.random() < p:
            R.add((x, y))

print(f"\n二元关系 R（包含 {len(R)} 个序偶）:")
# 按字典序打印 R
for pair in sorted(R, key=lambda p: (p[0], p[1])):
    print(f"  {pair}", end="")
print()

# 5. 从 R 中枚举所有双射（排列），检查序偶是否都在 R 中
all_perms = itertools.permutations(A)
valid_bijections = []   # 存储元组形式的排列
for perm in all_perms:
    # 检查该排列产生的所有序偶是否都属于 R
    if all((A[i], perm[i]) in R for i in range(n)):
        valid_bijections.append(perm)

if not valid_bijections:
    print("错误：R 中不存在任何双射，请检查生成逻辑。")
    exit()

# 随机选择一个双射作为 g
chosen_perm = random.choice(valid_bijections)
g = {A[i]: chosen_perm[i] for i in range(n)}

print("\n从 R 中抽取构造的双射 g:")
for x in A:
    print(f"  g({x}) = {g[x]}")

# 6. 构造 g 的逆函数 g⁻¹
g_inv = {g[x]: x for x in A}   # 双射，直接键值互换
print("\ng 的逆函数 g⁻¹:")
for y in A:
    print(f"  g⁻¹({y}) = {g_inv[y]}")

# 验证双射性及逆函数正确性
assert len(set(g.values())) == n, "g 不是单射"
assert set(g.values()) == set(A), "g 不是满射"
for x in A:
    assert g_inv[g[x]] == x, "逆函数错误"
print("\n双射性及逆函数验证通过。")