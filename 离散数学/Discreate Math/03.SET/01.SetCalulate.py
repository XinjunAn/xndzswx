#----------------------------------------------------------
# 集合并交差补运算
# 随机数生成两个任意集合，通过并交差补运算输出结果
#----------------------------------------------------------

import random
import string

# 1. 准备全集 E ----------
# 字符串形式，后面转为列表便于操作
letters = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
E = list(letters)                 # 全集用列表表示，便于遍历

# 2. 随机生成集合 A 和 B ----------
def random_subset(full_set, min_size=1, max_size=5):
    """从 full_set 中随机抽取 min_size~max_size 个不重复元素，返回列表"""
    size = random.randint(min_size, max_size)
    # 避免修改原全集，复制一份
    available = full_set[:]
    subset = []
    for _ in range(size):
        idx = random.randint(0, len(available) - 1)
        subset.append(available.pop(idx))   # 弹出以保证不重复
    return subset

A = random_subset(E)
B = random_subset(E)

# 确保 A 和 B 非空（random_subset 已保证至少1个元素）

# 3. 自行实现并交差补运算 ----------
#并集运算
def union(list1, list2):
    """并集：元素在 list1 或 list2 中，去掉重复元素"""
    result = []
    for x in list1:
        if x not in result:
            result.append(x)
    for x in list2:
        if x not in result:
            result.append(x)
    return result
#交集运算
def intersection(list1, list2):
    result = []
    for x in list1:
        if x in list2 and x not in result:
            result.append(x)
    return result
#差集运算
def difference(list1, list2):
    result = []
    for x in list1:
        if x not in list2 and x not in result:
            result.append(x)
    return result
#绝对补运算
def complement(subset, full_set):
    result = []
    for x in full_set:
        if x not in subset:
            result.append(x)
    return result

#对称差运算
def symmetric_difference(list1, list2):
    result = []
    result = difference(list1, list2)+difference(list2, list1)
    return result

# 执行运算
union_AB = union(A, B)
inter_AB = intersection(A, B)
diff_A_B = difference(A, B)
diff_B_A = difference(B, A)
comp_A = complement(A, E)
comp_B = complement(B, E)
symmetric_AB=symmetric_difference(A,B)
# ---------- 4. 输出结果 ----------
print("全集 E = {a, b, c, ..., z}  (共26个字母)")
print(f"集合 A = {sorted(A)}")
print(f"集合 B = {sorted(B)}")
print("\n--- 运算结果（自行实现，未用内置集合运算） ---")
print(f"A ∪ B  (并集)      = {sorted(union_AB)}")
print(f"A ∩ B  (交集)      = {sorted(inter_AB)}")
print(f"A - B  (差集)      = {sorted(diff_A_B)}")
print(f"B - A  (差集)      = {sorted(diff_B_A)}")
print(f"A 的补集 (E - A)   = {sorted(comp_A)}")
print(f"B 的补集 (E - B)   = {sorted(comp_B)}")
print(f"A与B的对称差 (A ⊕ B)   = {sorted(symmetric_AB)}")

#测试用例，随机函数生成