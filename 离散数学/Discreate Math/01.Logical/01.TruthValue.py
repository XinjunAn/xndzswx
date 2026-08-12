#------------------------------------------------------------
#该案例采用了真值表计算的方式，判断任意输入的命题公式的真值
#最后给出测试用例
#------------------------------------------------------------

#调用迭代器
import itertools
#调用正则表达式
import re

def generate_truth_table():
    print("="*50)
    print(" 欢迎使用命题逻辑真值表生成器 ".center(46, "="))
    print("="*50)
    print("【语法说明】")
    print("变元: 请使用单个大写字母 (如 P, Q, R)")
    print("非:  ~ 或 ! (如 ~P)")
    print("合取(与): & (如 P & Q)")
    print("析取(或): | (如 P | Q)")
    print("蕴含: -> (如 P -> Q)")
    print("等价: <-> (如 P <-> Q)")
    print("支持括号: ()")
    print("-" * 50)

    # 1. 从终端接收输入
    formula = input("请输入命题公式: ")

    # 2. 词法分析：提取所有大写字母作为变元，并去重排序
    variables = sorted(list(set(re.findall(r'[A-Z]', formula))))
    if not variables:
        print("错误: 未检测到有效的命题变元(大写字母)。")
        return

    # 3. 符号映射转换：将数学逻辑符号转换为 Python 可执行的代码
    py_formula = formula
    py_formula = py_formula.replace('<->', ' == ') # 等价映射
    py_formula = py_formula.replace('->', ' <= ')  # 蕴含映射 (布尔值中小于等于即为蕴含)
    py_formula = py_formula.replace('~', ' not ')
    py_formula = py_formula.replace('!', ' not ')
    py_formula = py_formula.replace('&', ' and ')
    py_formula = py_formula.replace('|', ' or ')

    # 4. 打印表头
    header_vars = "\t".join(variables)
    header_line = f"{header_vars}\t|\t{formula}"
    separator = "-" * (len(variables) * 8 + 8 + len(formula))
    print("\n" + separator)
    print(header_line)
    print(separator)

    # 5. 状态空间遍历与求值
    # 使用 itertools.product 生成 2^n 种 True/False 的组合
    for vals in itertools.product([False, True], repeat=len(variables)):
        # 将当前的真假值与变元名绑定成字典，例如 {'P': True, 'Q': False}
        env = dict(zip(variables, vals))
        
        try:
            # eval 在指定的环境(env)中动态执行字符串代码
            result = eval(py_formula, {}, env)
            
            # 格式化输出: 将 True/False 转为 T/F 以符合约定成俗的习惯
            row_str = "\t".join(['T' if v else 'F' for v in vals])
            res_str = 'T' if result else 'F'
            print(f"{row_str}\t|\t{res_str}")
            
        except Exception as e:
            print(f"解析错误, 请检查公式语法是否合法。详细错误: {e}")
            return
            
    print(separator + "\n")

# 运行主程序
if __name__ == "__main__":
    generate_truth_table()
#测试用例1：P->(Q|R)
#测试用例2：(A->B)|(C<->D)