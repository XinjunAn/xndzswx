import itertools

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

# 1 半群而非独异点: 正整数，op(a,b)=a+b+1
print("\n=== 1: 半群而非独异点 ===")
S_pos = [1,2,3,4,5]  # 取子集测试，但注意封闭性：1+2+1=4仍在集合内，但可能有溢出？我们可以只测试结合律
op_plus1 = lambda x,y: x+y+1
# 检查结合律（在有限子集上，如果值超出集合就不封闭，但仅测试结合律）
print("结合律(有限测试):", is_associative(S_pos, op_plus1))
# 查找单位元：要求 e+x+1=x => e+1=0 无解
e = find_identity(S_pos, op_plus1)
print("单位元:", e)  # None
print("=> 是半群，无单位元，不是独异点")

# 2 独异点而非群：自然数 0..n 加法
print("\n=== 2: 独异点而非群 ===")
N = [0,1,2,3,4]
add_N = lambda x,y: x+y  # 可能超出范围，但仍可验证单位元和逆元（限制在集合内）
print("封闭(有限会越界):", is_closed(N, add_N))  # 会False，因为2+3=5不在集合
# 实际要无限集，但我们仅作性质说明。可以改集合为 [0..∞] 抽象理解
# 这里只展示：单位元为0，但 1 的逆元 -1 不在自然数集中
print("单位元:", find_identity([0,1,2,3,4], lambda x,y: x+y))  # 0
print("因为非零元没有加法逆元在自然数中，所以不是群。")

# 3 非阿贝尔群：2x2 可逆矩阵 mod 2
print("\n=== 3: 非阿贝尔群 ===")
import numpy as np

# 定义所有 2x2 mod 2 的可逆矩阵（行列式不为0 mod2）
candidates = []
for a,b,c,d in itertools.product([0,1], repeat=4):
    det = (a*d - b*c) % 2
    if det != 0:
        candidates.append(np.array([[a,b],[c,d]]))
# 运算为矩阵乘法 mod 2
def mat_mul_mod2(A, B):
    return np.dot(A, B) % 2

# 检查群性质（仅针对几个元素验证非交换性）
A = np.array([[1,1],[0,1]])
B = np.array([[1,0],[1,1]])
print("A*B mod2:\n", mat_mul_mod2(A,B))
print("B*A mod2:\n", mat_mul_mod2(B,A))
print("乘法可交换?", np.array_equal(mat_mul_mod2(A,B), mat_mul_mod2(B,A)))
print("=> 构成非阿贝尔群（GL(2,2) 同构于 S3）")