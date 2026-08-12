#------------------------------------------------------------------
# 最大子序列（LIS）求解与Dilworth定理关联
#------------------------------------------------------------------
import random
def lis_with_sequence(nums):
    # 空序列
    if len(nums) == 0:
        return []
    # 复制nums序列，初始化为全1
    n = len(nums)
    dp = [1] * n
    # 前驱索引
    parent = [-1] * n  
    max_len = 1
    end_idx = 0
    i = 0
    # 遍历序列O（n^2）
    while i < n:
        j = 0
        # 最大子序列长度默认为1
        best = 1
        # 在<i 位置内遍历元素，找到初始最大子序列起始位置
        while j < i:
            if nums[j] < nums[i]:
                # 投票
                candidate = dp[j] + 1
                if candidate > best:
                    best = candidate
                    parent[i] = j  # 记录当前最优前驱
            j += 1
        dp[i] = best
        
        # 找全局最大
        if best > max_len:
            max_len = best
            end_idx = i
        i += 1
    
    # 回溯构建最大子序列
    result = []
    cur = end_idx
    while cur != -1:
        result.append(nums[cur])
        cur = parent[cur]
    
    # 反转找到的要输出的最大子序列
    reversed_result = []
    k = len(result) - 1
    while k >= 0:
        reversed_result.append(result[k])
        k -= 1
    
    return reversed_result

def main():
    n = int(input("请输入集合A的元素个数 n: "))   
    list= random.sample(range(n), n)
    print(list)
    print(lis_with_sequence(list))      
    
if __name__ == "__main__":
    main()