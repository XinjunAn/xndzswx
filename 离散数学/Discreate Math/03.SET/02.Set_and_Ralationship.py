#--------------------------------------------------------------
# 集合关系的判断 
# 解析集合输入，例如："{a,b,c}" 或 "a,b,c}"，返回字母列表（去重）
#--------------------------------------------------------------
def parse_set(prompt):
    s = input(prompt).strip()
    if s.endswith('}'):
        s = s[:-1]
    if s.startswith('{'):
        s = s[1:]
    elements = []
    for ch in s:
        if 'a' <= ch <= 'z' or '0' <= ch <= '9':
            if ch not in elements:
                elements.append(ch)
    return elements

# 判断 A 是否为 B 的子集
def is_subset(A, B):
    for x in A:
        if x not in B:
            return False
    return True

# 判断两个列表是否相等
def lists_equal(A, B):
    if len(A) != len(B):
        return False
    for x in A:
        if x not in B:
            return False
    return True

# 判断是否有交集（并集非空）
def has_intersection(A, B):
    for x in A:
        if x in B:
            return True
    return False

# 计算交集（用于显示）
def get_intersection(A, B):
    result = []
    for x in A:
        if x in B and x not in result:
            result.append(x)
    return sorted(result)

# 主程序
if __name__ == "__main__":
    A = parse_set("请输入集合 A（格式如 {a,b,c}）: ")
    B = parse_set("请输入集合 B（格式如 {a,b,c}）: ")

    if not A or not B:
        print("集合不能为空！")
        exit()

    print(f"集合 A = {sorted(A)}")
    print(f"集合 B = {sorted(B)}")

    # 关系判断并输出结论
    if lists_equal(A, B):
        print("结论：两个集合相等")
    elif is_subset(A, B):
        print("结论：B 包含 A")
    elif is_subset(B, A):
        print("结论：A 包含 B")
    elif not has_intersection(A, B):
        print("结论：两个集合交集为空")
    else:
        print("结论：两个集合相交（无包含关系）")
        inter = get_intersection(A, B)
        print(f"交集为：{inter}")

#测试用例1:A{a,c,b,2,1} B{2,1,a,c,b}
#测试用例1:A{a,c,b,2,2,1} B{2,1,a,c,b}
