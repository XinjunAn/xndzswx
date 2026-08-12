#--------------------------------------------------------------------
# 群中寻找特殊元素求解，
# 任意给定某个范围内的若干数，采用群论中方法求解三数之和为0，降低时间复杂度
#--------------------------------------------------------------------


import numpy as np

def auto_scan(low,high,size):
    #调用随机数，生成包含size和元素且在low和high之间的一个代数系统
    arr=np.random.randint(low, high, size)
    # 自动调用（快速）排序算法算法复杂度为O(n(logn))
    arr.sort()
    res=[]
    #遍历res表列，其算法复杂度为O(n^2)
    for i in range(size-2):
        if arr[i]>0:
            break
        if (i>0) and (arr[i]==arr[i-1]):
            continue
        l=i+1
        r=size-1
        while l<r:
            t=arr[i]+arr[l]+arr[r]
            if t==0:
                res.append([arr[i],arr[l],arr[r]])
                while l<r and arr[l]==arr[l+1]:
                    l+=1
                while l<r and arr[r]==arr[r-1]:
                    r-=1
                l+=1
                r-=1
            elif t<0:
                l+=1
            else:
                r-=1
    print(res)



if __name__ == "__main__":
    low= int(input(f"请输入起始值（最小值，建议是整数）"))
    high = int(input(f"请输入终止值（最大值，建议是整数）"))
    size = int(input(f"元素个数（不要少于3）")) 
    if 3<= size <=high-low:
        auto_scan(low,high,size)
    else:
        print("输入数据有误")
    
     