#----------------------------------------------
# 存在与全称量词组合使用的实例，寻找小镇上的法官
#----------------------------------------------
from typing import List

def findJudge(N: int, trust: List[List[int]]) -> int:
    """
    小镇法官问题：
    - 存在一个人 i，使得：
        全称量词，所有其他人都信任 i  (入度 == N-1)
        全称量词，i不信任任何人      (出度 == 0)
    """
    if N == 1:
        # 如果只有一个人且没有信任关系，他就是法官
        return 1 if not trust else -1

    # 被谁信任（入边）
    trusted_by = [set() for _ in range(N + 1)]
    # 信任谁（出边）
    trusts = [set() for _ in range(N + 1)]

    for a, b in trust:
        trusts[a].add(b)
        trusted_by[b].add(a)

    # 存在量词：尝试每一个人 i
    for i in range(1, N + 1):
        # 全称量词：所有其他人 j 都信任 i
        all_others_trust_i = all(j in trusted_by[i] for j in range(1, N + 1) if j != i)
        # 全称量词：i 不信任任何人 （等价于：不存在 i 信任的人）
        i_trusts_nobody = not any(True for _ in trusts[i])

        if all_others_trust_i and i_trusts_nobody:
            return i
    return -1   # 不存在满足条件的法官


# 示例用法
if __name__ == "__main__":
    # N = 3, trust = [[1,3],[2,3]]  -> 法官是 3
    print(findJudge(3, [[1, 3], [2, 3]]))  # 输出 3
    # N = 3, trust = [[1,3],[2,3],[3,1]] -> 没有法官
    print(findJudge(3, [[1, 3], [2, 3], [3, 1]]))  # 输出 -1
    # N = 1, trust = [] -> 法官是 1
    print(findJudge(1, []))  # 输出 1