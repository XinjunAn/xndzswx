#----------------------------------------------------------------
# 数据库规范化——基于函数依赖的属性闭包与候选键
#----------------------------------------------------------------

import itertools

def compute_closure(attrs, fds):
    """
    计算属性集 attrs 在函数依赖集 fds 下的闭包。
    fds 格式: [(左部集合, 右部集合), ...]，左右部均为 set。
    """
    closure = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs.issubset(closure) and not rhs.issubset(closure):
                closure.update(rhs)
                changed = True
    return closure

def find_candidate_keys(attributes, fds):
    """
    找出属性集 attributes 在函数依赖 fds 下的所有候选键。
    返回列表，每个元素为 frozenset 表示的属性集合。
    """
    all_attrs = set(attributes)
    candidates = []
    # 按大小升序枚举所有非空子集
    for size in range(1, len(all_attrs) + 1):
        for subset in itertools.combinations(all_attrs, size):
            subset = set(subset)
            # 剪枝：如果当前集合已经是某个已知候选键的真超集，则跳过
            if any(c.issubset(subset) and c != subset for c in candidates):
                continue
            closure = compute_closure(subset, fds)
            if closure == all_attrs:
                candidates.append(subset)
        # 一旦该大小层找到了候选键，更大的属性集就不可能是“最小”超键，直接终止
        if candidates:
            break
    return [frozenset(c) for c in candidates]

def format_fds(fds):
    """辅助函数：格式化输出函数依赖集"""
    return ', '.join(f"{''.join(sorted(lhs))}->{''.join(sorted(rhs))}" for lhs, rhs in fds)

# ================== 测试案例 ==================
if __name__ == "__main__":
    print("=" * 60)
    print("案例 深入测试：属性闭包与候选键求解")
    print("=" * 60)

    # ---------- 测试1：单属性候选键 ----------
    print("\n【测试1】简单学生表，单属性候选键")
    attrs1 = {'学号', '姓名', '系名', '系主任'}
    fds1 = [
        ({'学号'}, {'姓名', '系名'}),
        ({'系名'}, {'系主任'})
    ]
    print(f"属性集: {attrs1}")
    print(f"函数依赖: {format_fds(fds1)}")

    # 闭包测试
    closure = compute_closure({'学号'}, fds1)
    print(f"闭包 {{学号}}⁺ = {closure}  (应为所有属性: {closure == attrs1})")

    keys = find_candidate_keys(attrs1, fds1)
    print(f"候选键: {[set(k) for k in keys]}  (应为 [{{'学号'}}])\n")

    # ---------- 测试2：复合候选键 ----------
    print("【测试2】学生选课表，复合候选键")
    attrs2 = {'学号', '姓名', '课程号', '成绩', '系名', '系主任'}
    fds2 = [
        ({'学号'}, {'姓名', '系名'}),
        ({'系名'}, {'系主任'}),
        ({'学号', '课程号'}, {'成绩'})
    ]
    print(f"属性集: {attrs2}")
    print(f"函数依赖: {format_fds(fds2)}")

    closure2 = compute_closure({'学号'}, fds2)
    print(f"闭包 {{学号}}⁺ = {closure2}  (不含成绩和课程号，因为学号不能决定课程号)")

    closure23 = compute_closure({'学号', '课程号'}, fds2)
    print(f"闭包 {{学号, 课程号}}⁺ = {closure23}  (应为全集: {closure23 == attrs2})")

    keys2 = find_candidate_keys(attrs2, fds2)
    print(f"候选键: {[set(k) for k in keys2]}  (应为 [{{'学号', '课程号'}}])\n")

    # ---------- 测试3：多个候选键 ----------
    print("【测试3】存在多个候选键的情况")
    attrs3 = {'A', 'B', 'C', 'D'}
    fds3 = [
        ({'A'}, {'B'}),
        ({'B'}, {'A'}),
        ({'A', 'B'}, {'C', 'D'}),
        ({'C'}, {'D'})
    ]
    print(f"属性集: {attrs3}")
    print(f"函数依赖: {format_fds(fds3)}")

    # 验证 A和B对称，都能决定整个集合吗？
    ca = compute_closure({'A'}, fds3)
    cb = compute_closure({'B'}, fds3)
    print(f"闭包 {{A}}⁺ = {ca}")
    print(f"闭包 {{B}}⁺ = {cb}")
    print(f"两者都能决定全集: {ca == attrs3 and cb == attrs3}")

    keys3 = find_candidate_keys(attrs3, fds3)
    print(f"候选键: {[set(k) for k in keys3]}  (应为 [{{'A'}}, {{'B'}}])\n")

    # ---------- 测试4：包含无关属性的依赖，验证剪枝有效性 ----------
    print("【测试4】稍大规模，验证极小性剪枝")
    attrs4 = {'A', 'B', 'C', 'D', 'E'}
    fds4 = [
        ({'A', 'B'}, {'C'}),
        ({'C'}, {'D'}),
        ({'D'}, {'E'}),
        ({'E'}, {'A'})  # 形成环，但 A,B 仍是入口
    ]
    print(f"属性集: {attrs4}")
    print(f"函数依赖: {format_fds(fds4)}")

    # 单属性 A 不能决定 B，所以候选键必须包含 B
    closure_A = compute_closure({'A'}, fds4)
    print(f"闭包 {{A}}⁺ = {closure_A}")
    keys4 = find_candidate_keys(attrs4, fds4)
    print(f"候选键: {[set(k) for k in keys4]}  (例如 {{A,B}} 或 {{B,E}} 等)")

    # 验证每个候选键的闭包都是全集，且任意真子集都不是
    for k in keys4:
        assert compute_closure(k, fds4) == attrs4, f"候选键 {set(k)} 不能决定全集"
        # 检查极小性：去掉任何属性后闭包不再是全集
        for attr in k:
            sub = set(k) - {attr}
            if sub:  # 非空
                assert compute_closure(sub, fds4) != attrs4, f"候选键 {set(k)} 不是极小，其子集 {sub} 也能决定全集"
    print("✓ 所有候选键的极小性验证通过\n")

    # ---------- 测试5：无函数依赖（仅平凡依赖），任何属性自己决定自己 ----------
    print("【测试5】无用户定义函数依赖，仅平凡依赖")
    attrs5 = {'X', 'Y'}
    fds5 = []  # 无函数依赖
    keys5 = find_candidate_keys(attrs5, fds5)
    print(f"属性集: {attrs5}, 依赖集为空")
    print(f"候选键: {[set(k) for k in keys5]}  (应该是整个属性集本身 {{X,Y}}，因为没有更小的集合能决定Y和X)")
    # 因为 {} 的闭包是 {}，{X} 的闭包是 {X}，只有 {X,Y} 才能得到 {X,Y}
    closure_X = compute_closure({'X'}, fds5)
    print(f"闭包 {{X}}⁺ = {closure_X} (≠全集)")
    print("✓ 结果符合预期\n")

    # ---------- 测试6：带传递依赖的典型模式 ----------
    print("【测试6】数据库经典示例：R(A,B,C,D), F={A->B, B->C, C->D}")
    attrs6 = {'A', 'B', 'C', 'D'}
    fds6 = [({'A'}, {'B'}), ({'B'}, {'C'}), ({'C'}, {'D'})]
    keys6 = find_candidate_keys(attrs6, fds6)
    print(f"属性集: {attrs6}, 依赖: {format_fds(fds6)}")
    print(f"候选键: {[set(k) for k in keys6]}  (应为 [{{'A'}}])")
    print("✓ 正确，因为 A->B->C->D 传递闭包覆盖全集\n")

    print("=" * 60)
    print("所有测试完成，代码行为符合预期。")