import random
import string

def op(a, b):
    """
    定义运算规则：
    返回较长的字符串；长度相等时返回字典序较小者。
    """
    if len(a) > len(b):
        return a
    elif len(b) > len(a):
        return b
    else:
        # 长度相等，返回字典序较小者
        return a if a < b else b

def get_random_string():
    """生成长度在 1 到 5 之间的小写字母随机字符串"""
    length = random.randint(1, 5)
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def verify_associativity(trials=100000):
    """通过随机抽样验证结合律"""
    print(f"开始进行 {trials} 次随机抽样验证...")
    
    for _ in range(trials):
        a = get_random_string()
        b = get_random_string()
        c = get_random_string()
        
        # 计算 (a op b) op c
        left_result = op(op(a, b), c)
        # 计算 a op (b op c)
        right_result = op(a, op(b, c))
        
        # 如果不相等，说明找到了反例（不满足结合律）
        if left_result != right_result:
            print("❌ 发现不满足结合律的反例！")
            print(f"a = '{a}', b = '{b}', c = '{c}'")
            print(f"(a op b) op c = '{left_result}'")
            print(f"a op (b op c) = '{right_result}'")
            return False
            
    print("✅ 验证完毕：未找到任何反例。这在经验上证明了该运算【满足】结合律。")
    return True

if __name__ == "__main__":
    # 运行十万次测试
    verify_associativity(1000)