#------------------------------------------------------------
#该案例采用了真值表计算的方式，判断若干谓词公式是否推导出有效结论
#约定有限个体域，遍历所有谓词公式转为命题公式的结构，计算真值表
#最后给出测试用例
#------------------------------------------------------------



import re
from itertools import product

# 词法分析，约定输入的谓词公式的组织形式和符号
def tokenize(formula):
    """
    支持的符号：
        A. / forall / @    →  全称量词 ∀
        E. / exists / #    →  存在量词 ∃
        ~ / !              →  否定
        &                  →  合取
        |                  →  析取
        -> / <->           →  蕴含 / 双条件
        ( ) ,              →  分隔符
        大写字母开头        →  谓词符号（如 P, Q, Loves)
        小写字母为变元      →  个体变元或常量
    """
    tokens = []
    i = 0
    n = len(formula)

    while i < n:
        ch = formula[i]

        if ch.isspace():
            i += 1
            continue

        # 多字符符号优先级设置
        if formula.startswith("<->", i):
            tokens.append(("OP", "<->")); i += 3; continue
        if formula.startswith("->", i):
            tokens.append(("OP", "->")); i += 2; continue
        if formula.startswith("forall", i):
            tokens.append(("QUANT", "forall")); i += 6; continue
        if formula.startswith("exists", i):
            tokens.append(("QUANT", "exists")); i += 6; continue
        if formula.startswith("A.", i):
            tokens.append(("QUANT", "forall")); i += 2; continue
        if formula.startswith("E.", i):
            tokens.append(("QUANT", "exists")); i += 2; continue

        if ch == "@":
            tokens.append(("QUANT", "forall")); i += 1; continue
        if ch == "#":
            tokens.append(("QUANT", "exists")); i += 1; continue

        if ch in "~!":
            tokens.append(("OP", "~")); i += 1; continue
        if ch in "&|":
            tokens.append(("OP", ch)); i += 1; continue
        if ch in "(),":
            tokens.append((ch, ch)); i += 1; continue

        # 标识符：字母开头
        m = re.match(r"[A-Za-z][A-Za-z0-9_]*", formula[i:])
        if m:
            name = m.group(0)
            if name[0].isupper():
                tokens.append(("PRED", name))    # 谓词（大写开头）
            else:
                tokens.append(("IDENT", name))   # 变元/常量（小写开头）
            i += len(name)
            continue

        raise ValueError(f"无法识别的字符: {formula[i:]}")

    return tokens

# 构造AST（Abstract Syntax Tree），做语法分析实现递归下降构造
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def eat(self, kind=None, value=None):
        tk = self.peek()
        if tk[0] is None:
            raise ValueError("公式意外结束")
        if kind and tk[0] != kind:
            raise ValueError(f"期望类型 {kind}，实际 {tk}")
        if value and tk[1] != value:
            raise ValueError(f"期望 {value}，实际 {tk[1]}")
        self.pos += 1
        return tk

    def parse(self):
        node = self.parse_iff()
        if self.peek()[0] is not None:
            raise ValueError(f"多余符号: {self.peek()}")
        return node

    def parse_iff(self):
        node = self.parse_imp()
        while self.peek() == ("OP", "<->"):
            self.eat(); right = self.parse_imp()
            node = ("iff", node, right)
        return node

    def parse_imp(self):
        node = self.parse_or()
        if self.peek() == ("OP", "->"):
            self.eat(); right = self.parse_imp()   # 右结合
            node = ("imp", node, right)
        return node

    def parse_or(self):
        node = self.parse_and()
        while self.peek() == ("OP", "|"):
            self.eat(); right = self.parse_and()
            node = ("or", node, right)
        return node

    def parse_and(self):
        node = self.parse_unary()
        while self.peek() == ("OP", "&"):
            self.eat(); right = self.parse_unary()
            node = ("and", node, right)
        return node

    def parse_unary(self):
        tk = self.peek()
        if tk == ("OP", "~"):
            self.eat()
            return ("not", self.parse_unary())
        if tk[0] == "QUANT":
            return self.parse_quant()
        return self.parse_atom()

    def parse_quant(self):
        _, q = self.eat("QUANT")
        _, var = self.eat("IDENT")           # 量词后必须跟变元
        body = self.parse_unary()            # 量词作用于最近的一元式
        return (q, var, body)                # ("forall","x",body) 或 ("exists","x",body)

    def parse_atom(self):
        tk = self.peek()
        if tk == ("(", "("):
            self.eat("("); node = self.parse_iff(); self.eat(")")
            return node
        if tk[0] == "PRED":
            _, pname = self.eat("PRED")
            args = []
            if self.peek() == ("(", "("):    # P(x,y)
                self.eat("(")
                while True:
                    _, aname = self.eat("IDENT")
                    args.append(aname)
                    if self.peek() == (",", ","):
                        self.eat(","); continue
                    break
                self.eat(")")
            return ("pred", pname, tuple(args))
        raise ValueError(f"原子公式位置有误: {tk}")

# 语义分析：AST 求值（关键算法）
def substitute(node, var, const):
    """把 AST 中自由出现的 var 替换为常量 const（用于量词展开）"""
    kind = node[0]

    if kind == "pred":
        _, name, args = node
        new_args = tuple(const if a == var else a for a in args)
        return ("pred", name, new_args)

    if kind == "not":
        return ("not", substitute(node[1], var, const))

    if kind in ("and", "or", "imp", "iff"):
        return (kind, substitute(node[1], var, const), substitute(node[2], var, const))

    if kind in ("forall", "exists"):
        _, bound_var, body = node
        if bound_var == var:
            return node                         # 变量被内层重新绑定，不再替换
        return (kind, bound_var, substitute(body, var, const))

    return node


def ground_atom_key(name, args):
    """把 P(a,b) 转成字符串键 'P(a,b)'，作为命题变元名"""
    return f"{name}({','.join(args)})"


def collect_ground_atoms(node, domain, atoms):
    """
    遍历 AST，把所有可能的基原子（ground atom）加入集合。
    量词按论域展开时，会替换掉变量，最终 args 全是常量。
    """
    kind = node[0]

    if kind == "pred":
        _, name, args = node
        if all(a in domain for a in args):     # 只收集全常量的原子
            atoms.add(ground_atom_key(name, args))
        return

    if kind == "not":
        collect_ground_atoms(node[1], domain, atoms); return

    if kind in ("and", "or", "imp", "iff"):
        collect_ground_atoms(node[1], domain, atoms)
        collect_ground_atoms(node[2], domain, atoms); return

    if kind in ("forall", "exists"):
        _, var, body = node
        for c in domain:                       # 用论域中每个常量展开一遍
            collect_ground_atoms(substitute(body, var, c), domain, atoms)


def evaluate(node, domain, env):
    """
    在给定论域和真值环境下求值。
    env: {'P(a)': True, 'Q(b)': False, ...}
    """
    kind = node[0]

    if kind == "pred":
        _, name, args = node
        return env[ground_atom_key(name, args)]

    if kind == "not":
        return not evaluate(node[1], domain, env)

    if kind == "and":
        return evaluate(node[1], domain, env) and evaluate(node[2], domain, env)

    if kind == "or":
        return evaluate(node[1], domain, env) or evaluate(node[2], domain, env)

    if kind == "imp":
        return (not evaluate(node[1], domain, env)) or evaluate(node[2], domain, env)

    if kind == "iff":
        return evaluate(node[1], domain, env) == evaluate(node[2], domain, env)

    if kind == "forall":                       # ∀x φ(x)  ≡  φ(c₁) ∧ φ(c₂) ∧ ...
        _, var, body = node
        return all(evaluate(substitute(body, var, c), domain, env) for c in domain)

    if kind == "exists":                       # ∃x φ(x)  ≡  φ(c₁) ∨ φ(c₂) ∨ ...
        _, var, body = node
        return any(evaluate(substitute(body, var, c), domain, env) for c in domain)

    raise ValueError(f"未知节点: {node}")


# 剖分多个公式为单个的谓词公式，中间用逗号隔开
def split_formulas(raw):
    parts, cur, depth = [], [], 0
    for ch in raw:
        if ch == "," and depth == 0:
            parts.append("".join(cur).strip()); cur = []; continue
        if ch == "(": depth += 1
        elif ch == ")": depth -= 1
        cur.append(ch)
    parts.append("".join(cur).strip())
    if any(not p for p in parts):
        raise ValueError("存在空公式")
    return parts

#主控制逻辑程序
def main():
    print("=" * 65)
    print("           谓词逻辑推理证明器（Herbrand 有限域方法）")
    print("=" * 65)
    print("符号说明：")
    print("  量词：  forall x / A.x / @x        （全称）")
    print("          exists x / E.x / #x         （存在）")
    print("  联结词：~ (非)  & (与)  | (或)  -> (蕴含)  <-> (等值)")
    print("  谓词：  大写字母开头，如 P(x), Loves(x,y)")
    print("  变元：  小写字母，如 x, y, z")
    print("-" * 65)
    print("示例：A.x (P(x) -> Q(x)), P(a), Q(a)")
    print("-" * 65)

    try:
        raw = input("请输入公式序列（逗号分隔）：").strip()
        formulas = split_formulas(raw)
        if len(formulas) < 2:
            print("至少需要 1 个前提 + 1 个结论"); return

        # 解析所有公式为 AST
        asts = [Parser(tokenize(f)).parse() for f in formulas]
        premises_ast   = asts[:-1]
        conclusion_ast = asts[-1]

        # 读取论域
        dom_raw = input("请输入有限论域（如 a,b 或 a,b,c）：").strip()
        domain = tuple(x.strip() for x in dom_raw.split(",") if x.strip())
        if not domain:
            print("论域不能为空"); return

        # 收集所有 ground atom：谓词逻辑 → 命题逻辑
        atoms = set()
        for ast in asts:
            collect_ground_atoms(ast, domain, atoms)
        atoms = sorted(atoms)

        if not atoms:
            print("未发现任何原子公式"); return

        print(f"\n【论域】D = {{{', '.join(domain)}}}")
        print(f"【展开后的原子命题】共 {len(atoms)} 个：{atoms}")
        print(f"【真值表规模】2^{len(atoms)} = {2**len(atoms)} 行\n")

        if len(atoms) > 12:
            print(f"警告：原子数过多（{len(atoms)}），继续将非常慢。")
            if input("是否继续？(y/N): ").strip().lower() != "y":
                return

        # 打印表头
        headers = list(atoms) + [f"P{i+1}" for i in range(len(premises_ast))] + ["C", "有效?"]
        widths = [max(len(h), 5) for h in headers]
        fmt = " | ".join("{:^" + str(w) + "}" for w in widths)
        sep = "-+-".join("-" * w for w in widths)
        print(fmt.format(*headers))
        print(sep)

        valid = True
        counterexamples = []

        # 枚举所有真值指派（关键：把谓词逻辑归约到命题逻辑）
        for values in product([False, True], repeat=len(atoms)):
            env = dict(zip(atoms, values))

            prem_vals = [evaluate(ast, domain, env) for ast in premises_ast]
            conc_val  = evaluate(conclusion_ast, domain, env)
            all_prem  = all(prem_vals)
            row_valid = (not all_prem) or conc_val     # 有效当且仅当  A → C

            tf = lambda b: "T" if b else "F"
            row = [tf(env[a]) for a in atoms] + [tf(v) for v in prem_vals] + [tf(conc_val), tf(row_valid)]
            print(fmt.format(*row))

            if not row_valid:
                valid = False
                counterexamples.append({a: env[a] for a in atoms})

        # 最终结论
        print("\n" + "=" * 65)
        if valid:
            print("【结论】推理有效 ✔")
            print(f"在论域 {{{', '.join(domain)}}} 下，最后一个公式是前 {len(premises_ast)} 个公式的有效结论。")
            print("注意：本判定仅针对给定的有限论域；谓词逻辑的普遍有效性不可判定。")
        else:
            print("【结论】推理无效 ✘")
            print(f"发现 {len(counterexamples)} 个反模型（前提全真但结论为假）：")
            for i, ce in enumerate(counterexamples[:3], 1):
                sig = ", ".join(f"{k}={tf(v)}" for k, v in ce.items())
                print(f"  反例 {i}: {sig}")
            if len(counterexamples) > 3:
                print(f"  ... 还有 {len(counterexamples)-3} 个反例")

    except ValueError as e:
        print(f"错误：{e}")


if __name__ == "__main__":
    main()
    
    
#测试用例1：A.x(P(x)->Q(x)),P(a),Q(a)
#测试用例2：E.x(P(x))->A.x(Q(x)),A.x(P(x)->Q(x))