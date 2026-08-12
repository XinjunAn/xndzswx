#------------------------------------------------------------
#该案例测试迭代式求传递闭包和warshall算法求传递闭包在计算负责度的差异
#------------------------------------------------------------
# 调用随机函数包生成随机的矩阵
import random
#调用time函授包记录耗费的时钟
import time

# 1. 矩阵生成函数
def generate_matrix(n, m):
    # 所有可能的边 (i, j)
    all_pairs = [(i, j) for i in range(n) for j in range(n)]
    # 随机抽取 m 条边（无放回）
    chosen = random.sample(all_pairs, m)
    # 初始化矩阵
    mat = [[0]*n for _ in range(n)]
    for i, j in chosen:
        mat[i][j]=1
    #print("初始化的随机矩阵")
    #print(mat)
    #print()
    return mat

# 2. Warshall 算法（O(n³)）
def warshall_closure(mat,n):
    # 初始化一个临时矩阵
    new=[row[:] for row in mat]   

    for k in range(n):           # 列搜索作为中间节点
        for i in range(n):       # 行起点
            for j in range(n):  # 终点
                new[i][j]=new[i][j] or (new[i][k] and new[k][j])
    #print("warshall矩阵的最终结果")
    #print(new)

    return new

# 3. 传统迭代算法（布尔矩阵乘法，O(n⁴)）
def iterative_closure(mat,n):
    # 并集矩阵初始化
    cur = [row[:] for row in mat]     
    #next = [[0]*n for _ in range(n)]     

    for iters in range (n-1):
        #迭代求R^n矩阵，从R^2开始迭代
        next = [[0] * n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                #临时变量默认值为0
                if cur[i][k]:
                    for j in range(n):
                        if cur[k][j]:
                            next[i][j]=1
        #print("过渡矩阵R^",iters+2,next)
        #累计求R^n 的布尔代数和        
        for row in range(n):
            for col in range(n):
                cur[row][col]=cur[row][col] or next[row][col]
    #print("n^4迭代的最终结果")
    #print(cur)

    return cur

# 4. 主调用和输出时间的函数50

def main():
    print("=" * 60)
    print("传递闭包算法性能对比 (Warshall O(n³) vs 迭代法 O(n⁴))")
    print("=" * 60)

    try:
        n = int(input("\n请输入矩阵大小 n（建议 30~100，迭代法 n 不宜过大）："))
        if n <= 0:
            print("n 必须大于 0")
            return
        max_m = n * n
        m = int(input(f"请输入初始边数 m（< {max_m}，如 n²/4）："))
        if m < 0 or m >= max_m:
            print(f"m 必须在 0 ~ {max_m-1} 之间")
            return
    except ValueError:
        print("输入必须为整数")
        return

    # ---- 1. 生成矩阵 ----
    print(f"\n生成 {n}×{n} 矩阵，初始边数 m = {m} ...")
    mat = generate_matrix(n, m)

    # ---- 2. 运行 Warshall 算法 ----
    mat_w = [row[:] for row in mat]   # 复制，避免修改原矩阵
    start_w = time.perf_counter()
    new=warshall_closure(mat_w,n)
    elapsed_w = time.perf_counter() - start_w
    edges_w = sum(sum(row) for row in new)

    # ---- 3. 运行迭代法 ----
    print("\n开始运行迭代法（可能较慢，请耐心等待）...")
    start_iter = time.perf_counter()
    closure_iter = iterative_closure(mat,n)  # 传入原矩阵（内部会复制）
    elapsed_iter = time.perf_counter() - start_iter
    edges_iter = sum(sum(row) for row in closure_iter)

    # ---- 4. 输出结果 ----
    print("\n" + "-" * 60)
    print(f"Warshall 算法 (O(n³))：耗时 {elapsed_w:.6f} 秒，闭包边数 {edges_w}")
    print(f"迭代法     (O(n⁴))：耗时 {elapsed_iter:.6f} 秒，闭包边数 {edges_iter}")
    print(f"加速比 = {elapsed_iter / elapsed_w:.2f} 倍")
    print("=" * 60)

    # 验证两种结果是否一致
    if new == closure_iter:
        print("✅ 两种算法结果一致，闭包正确。")
    else:
        print("❌ 警告：两种算法结果不一致，请检查实现！")

if __name__ == "__main__":
    main()