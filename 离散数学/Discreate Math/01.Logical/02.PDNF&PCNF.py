#---------------------------------------------------------------------
#该案例采用了真值表计算的方式，输出任意输入的命题公式的主析取范式和主合取范式
#1.提取所有的命题变元组成大项和小项运算表，分别从中选择为真、为假的
#最后给出测试用例
#---------------------------------------------------------------------


#调用迭代器
import itertools
#调用正则表达式
import re

def parse_and_generate_normal_forms():
    #1.formula是输入的字符串——命题公式    
    formula = input("输入命题公式 (例如: P->(Q|R)): ")
   
    #2.提取公式中的命题变元，然后根据离散数学约定成俗的习惯排序成新的字符串
    variables=sorted(list(set(re.findall(r'[A-Z]', formula))))
    
    if not variables:
        print("错误: 未检测到有效的命题变元(大写字母)。")
        return
    num_vars = len(variables)
    #3.打印表头
    print(" 命题公式解析器：真值表与主范式生成 ".center(43, "="))
    
    #4.对variable字符串进行符号映射——将数学符号转为Python字符串
    #依次是双条件联结词<->/==转换为->、<=
    py_formula = formula.replace('<->','==').replace('->','<= ')
    #非联结词转换为！
    py_formula = py_formula.replace('~', ' not ').replace('!', ' not ')
    #合取联结词转换为&，析取联结词转换为|
    py_formula = py_formula.replace('&', ' and ').replace('|', ' or ')
    #print("py_formula=",py_formula)
    #5.打印表头
    print(" 真值表 (Truth Table) ".center(53, " "))
    print("-" * 60)
    #输出第一行的字符用Table键隔开8个字符
    header_vars = "\t".join(variables)
    print(f"Index\t|\t{header_vars}\t|\t{formula}")
    print("-" * 60)

    #分类存储True和False的表列，存储结构: (十进制索引i, [变量真假值的列表])
    true_rows = []  
    false_rows = [] 
    
    #5.状态空间遍历 (生成 2^n 种组合)
    for i,vals in enumerate(itertools.product([False, True], repeat=num_vars)):
        env = dict(zip(variables, vals))
        #print(env)
        try:
            result = eval(py_formula, {}, env)            
            # 打印真值表行 (F/T 格式)
            row_str = "\t".join(['T' if v else 'F' for v in vals])
            res_str = 'T' if result else 'F'
            print(f"{i}\t|\t{row_str}\t|\t{res_str}")
            
            # 根据结果分类
            if result:
                true_rows.append((i, vals))
            else:
                false_rows.append((i, vals))
                
        except Exception as e:
            print(f"\n解析错误, 请检查语法。详情: {e}")
            return
            
    print("-" * 60)
    
    #6.生成主析取范式 (PDNF-极小项之和)
    if not true_rows:
    #原命题公式为矛盾式
        pdnf_str="F (无极小项)"
        pdnf_math="∅"
    else:
        minterms=[]
        indices=[]
        for idx,vals in true_rows:
            indices.append(str(idx))
            term=[]
            for var, val in zip(variables, vals):
                # 极小项构造：值为True保留原变量，值为False加否定(~)
                term.append(var if val else f"!{var}")
            # 内部用 & 连接
            minterms.append("(" + " & ".join(term) + ")")
        
        # 外部用 | 连接
        pdnf_str = " | ".join(minterms)
        pdnf_math = f"∑ m({','.join(indices)})"

    #7.生成主合取范式(PCNF-极大项之积)
    if not false_rows:
    #原命题公式为永真式
        pcnf_str = "T (无极大项)"
        pcnf_math = "∅"
    else:
        maxterms = []
        indices = []
        for idx, vals in false_rows:
            indices.append(str(idx))
            term = []
            for var, val in zip(variables, vals):
                # 极大项构造：值为False保留原变量，值为True加否定(~) -> 逆向逻辑!
                term.append(var if not val else f"!{var}")
            # 内部用 | 连接
            maxterms.append("(" + " | ".join(term) + ")")
      
        # 外部用 & 连接
        pcnf_str = " & ".join(maxterms)
        pcnf_math = f"∏ M({','.join(indices)})"

    # 打印最终结果
    print("\n" + "="*60)
    print(" 范式计算结果 ".center(48, " "))
    print("="*60)
    print(f"【主析取范式 (PDNF)】\n表达式: {pdnf_str}\n简记法: {pdnf_math}\n")
    print(f"【主合取范式 (PCNF)】\n表达式: {pcnf_str}\n简记法: {pcnf_math}\n")
    
    # 永真/永假判断
    if not false_rows:
        print("结论: 该公式为【重言式 】")
    elif not true_rows:
        print("结论: 该公式为【矛盾式 】")
    else:
        print("结论: 该公式为【可满足式 】")

if __name__ == "__main__":
    parse_and_generate_normal_forms()
#测试用例1：(P->Q)<->R
#测试用例2：(A-B)&(A->C)