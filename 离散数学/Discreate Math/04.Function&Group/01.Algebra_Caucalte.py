#------------------------------------------------
# 在一个模为8的加法运算上判断是否构成半群、独异点、群
# 现代密码学的运算理论基础
#------------------------------------------------
# 检查运算是否封闭
def is_closed(S, op):
    #遍历二元运算的结果是否在s 集合内（in 运算）
    for a in S:
        for b in S:
            if op(a, b) not in S:
                return False
    return True

# 判断是否构成半群（封闭 + 结合律）
def is_semigroup(S, op):
    # 首先判断是否封闭
    if not is_closed(S, op):
        return False
    # 三重循环判断是否满足结合特性
    for a in S:
        for b in S:
            for c in S:
                if op(op(a, b), c) != op(a, op(b, c)):
                    return False
    return True

# 判断是否构成独异点，返回(是否, 单位元)
def is_monoid(S, op):
    # 首先判断是否满足半群特性
    if not is_semigroup(S, op):
        return False, None
    # 寻找幺元e：对所有a有 e*a = a*e = a
    for e in S:
        if all(op(e, a) == a and op(a, e) == a for a in S):
            return True, e
    return False, None

# 判断是否构成群，返回(是否, 单位元)
def is_group(S, op):
    # 首先判断是否满足独异点（含幺半群）特性
    is_mon, identity = is_monoid(S, op)
    if not is_mon:
        return False, None
    # 检查每个元素是否有逆元
    for a in S:
        has_inverse = False
        for b in S:
            if op(a, b) == identity and op(b, a) == identity:
                has_inverse = True
                break
        if not has_inverse:
            return False, None
    return True, identity

# ===== 示例：模8 构造一个代数运算=====
Z8 = [0, 1, 2, 3, 4, 5, 6, 7]
add_mod8 = lambda x, y: (x + y) % 8

print("集合: Z8 =", Z8)
print("运算: a [+]8 b = (a+b) mod 8")
print("封闭性:", is_closed(Z8, add_mod8))
print("是半群:", is_semigroup(Z8, add_mod8))
monoid_result, identity = is_monoid(Z8, add_mod8)
print("是独异点:", monoid_result, " 单位元:", identity)
group_result, identity = is_group(Z8, add_mod8)
print("是群:", group_result, " 单位元:", identity)