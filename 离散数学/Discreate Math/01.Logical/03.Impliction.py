#------------------------------------------------------------
#该案例采用了真值表计算的方式，实现若干有效前件是否能推导出有效结论
#------------------------------------------------------------

#调用迭代器
import itertools
#调用正则表达式
import re

#规定了输入命题公式联结词符号的转换形式
OPERATORS = {"~", "!", "&", "|", "->", "<->", "(", ")"}

#剖分输入的字符串，逗号为分割不同的命题公式
def split_formulas(raw):
    parts = []
    current = []
    depth = 0
    #逗号分隔不同的命题公式
    for ch in raw:
        if ch == "," and depth == 0:
            part = "".join(current).strip()
            if not part:
                raise ValueError("逗号之间不能为空")
            parts.append(part)
            current = []
            continue
        #计算括号，并提高运算优先级
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                raise ValueError("括号不匹配")

        current.append(ch)
    if depth != 0:
        raise ValueError("括号不匹配")
    #合并新的命题公式字符串，删除输入中出现的空格字符
    part = "".join(current).strip()
    if not part:
        raise ValueError("最后一个公式不能为空")
    parts.append(part)
    #输出中间结果，是删除空格的命题公式字符串
    print(parts)   
    return parts

#把输入的命题公式字符串拆分为不同的token，便于后续计算每一个token的真值
def tokenize(formula):
    tokens = []
    i = 0
    n = len(formula)
    while i < n:
        ch = formula[i]
        if ch.isspace():
            i += 1
            continue

        if formula.startswith("<->", i):
            tokens.append("<->")
            i+= 3
        elif formula.startswith("->", i):
            tokens.append("->")
            i+= 2
        elif ch in "()~!&|":
            tokens.append(ch)
            i+= 1
        else:
            #要求输入的命题公式字符串全部采用大写字符，否则判定出错
            m = re.match(r"[A-Z]*", formula[i:])
            if not m:
                raise ValueError(f"无法识别的符号: {formula[i:]}")
            token = m.group(0)
            tokens.append(token)
            i += len(token)
    print("tokens=",tokens)
    return tokens

#判断输入的字符串是操作数还是操作符
def is_var(token):
    return token not in OPERATORS

#构造的规范化表达形式，每个命题公式以逆波兰式形式表示
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, expected=None):
        token = self.current()
        if token is None:
            raise ValueError("公式不完整")
        if expected is not None and token != expected:
            raise ValueError(f"期望 {expected}，实际得到 {token}")
        self.pos += 1
        return token

    def parse(self):
        node = self.parse_iff()
        if self.current() is not None:
            raise ValueError(f"存在多余符号: {self.current()}")
        return node

    #确定双条件运算<->为最低优先级
    def parse_iff(self):
        node = self.parse_imp()
        while self.current() == "<->":
            self.eat("<->")
            right = self.parse_imp()
            node = ("iff", node, right)
        return node

    #确定条件运算-> 优先级
    def parse_imp(self):
        node = self.parse_or()
        if self.current() == "->":
            self.eat("->")
            right = self.parse_imp()
            node = ("imp", node, right)
        return node
    #确定析取联结词运算优先级
    def parse_or(self):
        node = self.parse_and()
        while self.current() == "|":
            self.eat("|")
            right = self.parse_and()
            node = ("or", node, right)
        return node

   #确定合取联结词运算优先级
    def parse_and(self):
        node = self.parse_not()
        while self.current() == "&":
            self.eat("&")
            right = self.parse_not()
            node = ("and", node, right)
        return node
    #确定非联结词优先级
    def parse_not(self):
        token = self.current()
        if token in ("~", "!"):
            self.eat()
            child = self.parse_not()
            return ("not", child)
        return self.parse_atom()

    #确定()的优先级
    def parse_atom(self):
        token = self.current()
        if token == "(":
            self.eat("(")
            node = self.parse_iff()
            self.eat(")")
            return node
        if token is not None and is_var(token):
            self.eat()
            return ("var", token)
        raise ValueError("原子公式或括号位置有误")

#从每个token中取出字串，计算真值
def eval_ast(node, env):
    kind = node[0]

    if kind == "var":
        return env[node[1]]
    if kind == "not":
        return not eval_ast(node[1], env)
    if kind == "and":
        return eval_ast(node[1], env) and eval_ast(node[2], env)
    if kind == "or":
        return eval_ast(node[1], env) or eval_ast(node[2], env)
    if kind == "imp":
        return (not eval_ast(node[1], env)) or eval_ast(node[2], env)
    if kind == "iff":
        return eval_ast(node[1], env) == eval_ast(node[2], env)

    raise ValueError("未知语法树结点")


def collect_vars(node, var_set):
    kind = node[0]

    if kind == "var":
        var_set.add(node[1])
    elif kind == "not":
        collect_vars(node[1], var_set)
    else:
        collect_vars(node[1], var_set)
        collect_vars(node[2], var_set)

#规定的运算真值
def tf(x):
    return "T" if x else "F"


def main():
    
    try:
        #输入命题公式的字符串
        raw = input("请输入命题公式，逗号分隔（例如:P|Q,Q->R,P->S,!S,R&(P|Q)），最后一个为结论: ").strip()
        #调用剖分函数，删除字符串中的所有空格
        formulas = split_formulas(raw)
        #命题公式字符小于2意味着不可能有蕴含公式
        if len(formulas) < 2:
            print("至少需要输入一个前提和一个结论。")
            return

        ast_list = []
        for f in formulas:
            tokens = tokenize(f)
            #为每个tokens构造一个类似于栈的容器，包含操作符和操作数
            ast = Parser(tokens).parse()
            print("ast=",ast)
            ast_list.append(ast)
        #命题公式表达式列表中从头开始，一直到倒数第二个元素
        premises_str = formulas[:-1]
        #命题公式表达式的真值/结论
        conclusion_str = formulas[-1]
        #每个命题公式构造栈字符串        
        premises_ast = ast_list[:-1]
        #每个命题公式构造栈的真值
        conclusion_ast = ast_list[-1]

        var_set = set()
        for ast in ast_list:
            collect_vars(ast, var_set)
        variables = sorted(var_set)

        if not variables:
            print("没有检测到命题变元。")
            return

        print("\n前提:")
        for i, p in enumerate(premises_str, 1):
            print(f"P{i}: {p}")
        print(f"结论: {conclusion_str}")

        premise_conj_str = " ∧ ".join(f"({p})" for p in premises_str)
        print(f"检验公式: ¬({premise_conj_str}) ∨ ({conclusion_str})\n")

        headers = variables + [f"P{i}" for i in range(1, len(premises_str) + 1)] + ["A", "C", "¬A∨C"]
        widths = [max(4, len(h)) for h in headers]
        fmt = " | ".join("{:^" + str(w) + "}" for w in widths)
        sep = "-+-".join("-" * w for w in widths)

        print(fmt.format(*headers))
        print(sep)

        valid = True
        counterexamples = []

        for values in itertools.product([False, True], repeat=len(variables)):
            env = dict(zip(variables, values))

            premise_vals = [eval_ast(ast, env) for ast in premises_ast]
            a_val = all(premise_vals)
            c_val = eval_ast(conclusion_ast, env)
            target_val = (not a_val) or c_val

            row = [tf(env[v]) for v in variables]
            row += [tf(x) for x in premise_vals]
            row += [tf(a_val), tf(c_val), tf(target_val)]

            print(fmt.format(*row))

            if not target_val:
                valid = False
                counterexamples.append(", ".join(f"{v}={tf(env[v])}" for v in variables))

        print()
        if valid:
            print("结论: 有效")
            print("最后一个命题公式是前 n-1 个命题公式的有效结论。")
        else:
            print("结论: 无效")
            print("存在反例，使前提全真而结论为假：")
            for i, ce in enumerate(counterexamples, 1):
                print(f"反例{i}: {ce}")

    except ValueError as e:
        print("输入错误:", e)


if __name__ == "__main__":
    main()   
    
#测试用例1：P->!Q,!R|Q,R&!S,!P
#测试用例2：P|Q,Q->R,P->S,!S,R&(P|Q)