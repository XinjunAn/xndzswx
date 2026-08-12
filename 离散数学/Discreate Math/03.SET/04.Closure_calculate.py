#------------------------------------------------------------
#该案例是计算A集合上任意关系R的自反、对称闭包和warshall求解传递闭包的算法
#------------------------------------------------------------
# 调用随机函数包生成随机的矩阵
import random

#生成自反闭包
def reflexive_closure(R, n):
    R_ref = set(R)
    for i in range(n):
        R_ref.add((i, i))
    return R_ref

#生成对称闭包
def symmetric_closure(R):
    R_sym = set(R)
    for (x, y) in R:
        R_sym.add((y, x))
    return R_sym

#生成传递闭包
def transitive_closure(R, n):
    # 1.初始化 n×n邻接矩阵，1表示存在关系，0 表示不存在
    mat = [[0] * n for _ in range(n)]
    # 2.原始矩阵
    for x, y in R:
        mat[x][y] = 1
    # 3.wars hall算法迭代计算    
    for k in range(n):
        for i in range(n):
            if mat[i][k]:
                for j in range(n):
                    if mat[k][j]:
                        mat[i][j] = 1
    R_trans = set()
    for i in range(n):
        for j in range(n):
            if mat[i][j]:
                R_trans.add((i, j))
    return R_trans

def print_relation(R, n, title):
    print(f"\n{title}:")
    sorted_pairs = sorted(R)
    print("关系集合 =", sorted_pairs)
    mat = [[0] * n for _ in range(n)]
    for x, y in R:
        mat[x][y] = 1
    for row in mat:
        print(' '.join(str(v) for v in row))

def main():
    # 输入 n
    while True:
        try:
            n = int(input("请输入集合 A 的元素个数 n："))
            if n <= 0:
                print("n 必须为正整数，请重新输入。")
                continue
            break
        except ValueError:
            print("请输入一个整数。")

    # 输入 m
    max_m = n * n
    while True:
        try:
            m = int(input(f"请输入关系序偶的个数 m（m < {max_m}）："))
            if m < 0 or m >= max_m:
                print(f"m 必须在 0 到 {max_m-1} 之间，请重新输入。")
                continue
            break
        except ValueError:
            print("请输入一个整数。")

    # 随机生成 m 个不重复序偶
    all_pairs = [(i, j) for i in range(n) for j in range(n)]
    R = set(random.sample(all_pairs, m))

    # 输出原始关系
    print_relation(R, n, "原始关系 R")

    # 计算并输出三个闭包
    R_ref = reflexive_closure(R, n)
    R_sym = symmetric_closure(R)
    R_trans = transitive_closure(R, n)

    print_relation(R_ref, n, "自反闭包")
    print_relation(R_sym, n, "对称闭包")
    print_relation(R_trans, n, "传递闭包")

if __name__ == "__main__":
    main()
#测试用例：输入两个任意正整数，不宜太大。