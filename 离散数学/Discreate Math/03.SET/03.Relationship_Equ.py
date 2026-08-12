#------------------------------------------------------------
# 关系等级与否，通过遍历所有的序偶判断两个关系是否等价
#------------------------------------------------------------
# 调用正则表达式
import re

def parse_relation(prompt):
    """
    解析关系输入。
    支持格式：
      - {(a,1),(b,2)}   （圆括号序偶）
      - {(a,c),{b,c},{c,d}} （花括号序偶）
    序偶内部用逗号分隔前后元素。
    """
    s = input(prompt).strip()
    # 去除最外层可能的花括号（集合符号）
    if s.startswith('{') and s.endswith('}'):
        s = s[1:-1]

    # 匹配 (x,y) 或 {x,y} 形式的序偶
    pattern = r'[\(\{]([^\)\}]+)[\)\}]'
    matches = re.findall(pattern, s)
    pairs = []
    for match in matches:
        parts = match.split(',')
        if len(parts) == 2:
            x = parts[0].strip()
            y = parts[1].strip()
            if x and y:
                pair = (x, y)
                if pair not in pairs:   # 去重
                    pairs.append(pair)
    return pairs

def relations_equal(R1, R2):
    """显式比较两个关系是否相等（序偶前后元素严格匹配）"""
    if len(R1) != len(R2):
        return False, f"长度不等（R1: {len(R1)} 个序偶, R2: {len(R2)} 个）"

    matched = [False] * len(R2)
    for a1, b1 in R1:
        found = False
        for j, (a2, b2) in enumerate(R2):
            if not matched[j] and a1 == a2 and b1 == b2:
                matched[j] = True
                found = True
                break
        if not found:
            return False, f"序偶 ({a1},{b1}) 在 R1 中但不在 R2 中"
    return True, "所有序偶一一对应且严格相等"

# 主程序
if __name__ == "__main__":
    R1 = parse_relation("请输入关系 R1（如 {(a,1),(b,2)}）: ")
    R2 = parse_relation("请输入关系 R2（如 {(a,1),(b,2)}）: ")

    if not R1 or not R2:
        print("关系不能为空！")
        exit()

    print(f"解析后 R1 = {R1}")
    print(f"解析后 R2 = {R2}")

    equal, msg = relations_equal(R1, R2)
    if equal:
        print("结论：R1 和 R2 相等")
    else:
        print(f"结论：R1 和 R2 不相等\n原因：{msg}")
#测试用例1：    A{(a,b),(c,d),(d,c)}   B{(a,b),(d,x),(c,d)}
#测试用例2：    A{(a,1),(c,2),(d,3)}   B{(a,1),(d,2),(c,3)}