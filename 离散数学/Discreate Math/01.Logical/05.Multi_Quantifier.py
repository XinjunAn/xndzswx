#-----------------------------------------------------------------------------------------------
#多重量词嵌套使用的实例：非空集合A，B，C上构造的二元关系<x,y>∈A×B，且<y,z>∈B×C，判断是否所有的<x,z>∈A×C？
#------------------------------------------------------------------------------------------------


def is_composite_full(A: set, B: set, C: set, R: set, S: set, verbose=False) -> bool:
    """
    判断是否 ∀x∈A, ∀z∈C, ∃y∈B 使得 (x,y)∈R 且 (y,z)∈S
    若 verbose=True，则打印每个 x,z 组合的验证细节。
    """
    for x in A:
        for z in C:
            # 存在量词：是否存在 y 满足条件
            candidates = [y for y in B if (x, y) in R and (y, z) in S]
            if verbose:
                print(f"检查 ({x}, {z}): 满足条件的 y ∈ {candidates}")
            if not candidates:   # 即 not any(...)
                return False
    return True


# ========== 复杂测试用例 ==========
if __name__ == "__main__":
    # 定义非空集合，元素为有意义的字符串
    Students = {'小明', '小红', '小刚'}          # A
    Courses  = {'数学', '物理', '化学'}          # B
    Grades   = {'优秀', '良好', '及格'}          # C

    # --- 测试 1：预期返回 True ---
    # 构造 R ⊆ Students × Courses （学生选课）
    R1 = {('小明', '数学'), ('小明', '物理'),
          ('小红', '数学'), ('小红', '化学'),
          ('小刚', '物理'), ('小刚', '化学')}
    # 构造 S ⊆ Courses × Grades （课程可能获得的成绩）
    S1 = {('数学', '优秀'), ('数学', '良好'),
          ('物理', '良好'), ('物理', '及格'),
          ('化学', '优秀'), ('化学', '及格')}

    print("=== 测试 1：应该为 True ===")
    print(f"学生集合: {Students}")
    print(f"课程集合: {Courses}")
    print(f"成绩集合: {Grades}")
    print(f"选课关系 R: {R1}")
    print(f"成绩关系 S: {S1}")
    result1 = is_composite_full(Students, Courses, Grades, R1, S1, verbose=True)
    print(f"结果: 是否 ∀学生∀成绩 ∃课程 满足条件？ -> {result1}\n")

    # --- 测试 2：预期返回 False（破坏一个组合）---
    # 在 R2 中去掉一条边，使得某个 (学生,成绩) 无法通过任何课程连接
    R2 = R1 - {('小红', '数学')}   # 小红不再选数学
    print("=== 测试 2：应该为 False ===")
    print(f"选课关系 R (修改后): {R2}")
    result2 = is_composite_full(Students, Courses, Grades, R2, S1, verbose=True)
    print(f"结果: 是否 ∀学生∀成绩 ∃课程 满足条件？ -> {result2}\n")

    # --- 测试 3：更复杂，A,B,C 元素数增大 ---
    A3 = {'A1','A2','A3','A4'}
    B3 = {'B1','B2','B3','B4','B5'}
    C3 = {'C1','C2','C3'}
    # 构造覆盖所有 A×C 的 R,S
    R3 = set()
    # 让每个 A 都与所有 B 相连（完全图）
    for a in A3:
        for b in B3:
            R3.add((a, b))
    # S 需要确保对于任意 a,c，存在 b 使得 (a,b)∈R 且 (b,c)∈S。
    # 由于每个 a 连所有 b，只要每个 c 至少有一个 b 能到达它即可。
    S3 = {('B1','C1'), ('B2','C2'), ('B3','C3'),
          ('B4','C1'), ('B5','C2')}   # 每个 C 都有至少一个 B 与之相连
    print("=== 测试 3：更大集合 ===")
    print(f"|A|={len(A3)}, |B|={len(B3)}, |C|={len(C3)}")
    # 不逐条打印验证，直接用
    result3 = is_composite_full(A3, B3, C3, R3, S3)
    print(f"结果: {result3}")   # True

    # 破坏：移除一条 B→C 的边，使某个 C 没有 B 能连接
    S3_broken = S3 - {('B3','C3')}   # 现在 C3 没有 b 能连到（因为只有 B3 连 C3）
    result3b = is_composite_full(A3, B3, C3, R3, S3_broken)
    print(f"移除 ('B3','C3') 后: {result3b}")   # False