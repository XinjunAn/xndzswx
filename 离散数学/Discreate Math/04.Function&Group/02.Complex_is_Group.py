S_complex = [1+0j, -1+0j, 1j, -1j]
mul_complex = lambda x,y: x*y

def is_closed(S, op):
    return all(op(a,b) in S for a in S for b in S)

def is_associative(S, op):
    return all(op(op(a,b),c) == op(a,op(b,c)) for a in S for b in S for c in S)

def find_identity(S, op):
    for e in S:
        if all(op(e,a)==a and op(a,e)==a for a in S):
            return e
    return None

def has_inverses(S, op, identity):
    for a in S:
        if not any(op(a,b)==identity and op(b,a)==identity for b in S):
            return False
    return True

def inverse_of(S, op, identity, a):
    for b in S:
        if op(a,b)==identity and op(b,a)==identity:
            return b
    return None

print("\n=== 习题2: 复数单位根 ===")
print("封闭:", is_closed(S_complex, mul_complex))
print("结合律:", is_associative(S_complex, mul_complex))
id_c = find_identity(S_complex, mul_complex)
print("单位元:", id_c)
if id_c is not None:
    inv_ok = has_inverses(S_complex, mul_complex, id_c)
    print("每个元素有逆元:", inv_ok)
    if inv_ok:
        print("=> 构成群")
        # 检查循环性
        generators = []
        for g in S_complex:
            gen_set = {g**k for k in range(len(S_complex))}  # 生成 k=0..3
            if gen_set == set(S_complex):
                generators.append(g)
        print("循环群生成元:", generators)