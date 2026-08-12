#-------------------------------------------------------------
# 网络工程中的“高可用性(HA)拓扑”设计
#-------------------------------------------------------------

import itertools

class NetworkHATopology:
    def __init__(self):
        # 定义网络节点变量名
        self.nodes = ['SW', 'RA', 'RB', 'ISP1', 'ISP2']

    def evaluate_proposition(self, state: dict) -> bool:
        """
        离散数学命题求值：
        Formula: SW ∧ (RA ∨ RB) ∧ (ISP1 ∨ ISP2)
        """
        sw = state['SW']
        ra = state['RA']
        rb = state['RB']
        isp1 = state['ISP1']
        isp2 = state['ISP2']
        
        # 逻辑命题实现
        return sw and (ra or rb) and (isp1 or isp2)

    def generate_truth_table(self):
        """
        生成离散数学真值表，分析所有 2^5 = 32 种网络状态
        """
        print(f"{'SW':<6} | {'RA':<6} | {'RB':<6} | {'ISP1':<6} | {'ISP2':<6} || {'System Available':<15}")
        print("-" * 65)
        
        # 生成所有布尔组合的笛卡尔积 (True/False)
        combinations = list(itertools.product([True, False], repeat=len(self.nodes)))
        
        # 统计高可用性指标
        total_scenarios = len(combinations)
        available_scenarios = 0

        for combo in combinations:
            state = dict(zip(self.nodes, combo))
            result = self.evaluate_proposition(state)
            if result:
                available_scenarios += 1
                
            # 格式化输出 (T=True/UP, F=False/DOWN)
            row = [f"{'UP' if v else 'DOWN':<6}" for v in combo]
            res_str = "YES (Network UP)" if result else "NO (Network DOWN)"
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} || {res_str}")
            
        print("-" * 65)
        availability_rate = (available_scenarios / total_scenarios) * 100
        print(f"理论系统抗灾存活率: {available_scenarios}/{total_scenarios} ({availability_rate:.2f}%)")


# -------------------
# 测试用例执行模块
# -------------------
def run_specific_test_cases(network: NetworkHATopology):
    print("\n>>> 执行特定网络故障测试用例 (Test Cases) <<<")
    
    test_cases = [
        {
            "name": "TestCase 1: 完美状态 (所有设备正常)",
            "state": {'SW': True, 'RA': True, 'RB': True, 'ISP1': True, 'ISP2': True},
            "expected": True
        },
        {
            "name": "TestCase 2: 路由器与链路交叉故障 (RA宕机, ISP2断线 - 冗余生效)",
            "state": {'SW': True, 'RA': False, 'RB': True, 'ISP1': True, 'ISP2': False},
            "expected": True
        },
        {
            "name": "TestCase 3: 单点故障触发 (接入交换机 SW 宕机)",
            "state": {'SW': False, 'RA': True, 'RB': True, 'ISP1': True, 'ISP2': True},
            "expected": False
        },
        {
            "name": "TestCase 4: HA层完全崩溃 (两条ISP链路全部中断)",
            "state": {'SW': True, 'RA': True, 'RB': True, 'ISP1': False, 'ISP2': False},
            "expected": False
        }
    ]

    for tc in test_cases:
        actual = network.evaluate_proposition(tc['state'])
        status = "PASSED" if actual == tc['expected'] else "FAILED"
        print(f"[{status}] {tc['name']}")
        print(f"   输入状态: {tc['state']}")
        print(f"   预期输出: {tc['expected']} | 实际输出: {actual}\n")

if __name__ == "__main__":
    ha_network = NetworkHATopology()
    
    # 1. 运行具体测试用例
    run_specific_test_cases(ha_network)
    
    # 2. 生成离散数学真值表 (可选，输出所有32种状态)
    print("\n>>> 生成状态表（真值表/Truth Table)- 部分展示 <<<")
    ha_network.generate_truth_table()