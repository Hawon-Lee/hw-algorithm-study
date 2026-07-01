# https://leetcode.com/problems/same-tree/

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:

        # DFS 풀이
        def _dfs(p, q):
            p_queue = [p]
            q_queue = [q]
            
            while p_queue:
                p = p_stack.pop(-1)
                q = q_stack.pop(-1)

                if p is None and q is None:
                    continue
                if p is None or q is None:
                    return False
                
                if p.val != q.val:
                    return False
            
                p_queue += [p.left, p.right]
                q_queue += [q.left, q.right]
            
            return True

        return _dfs(p, q)


        # # 재귀 풀이
        # def _recur(p, q):
        #     # 종료 조건 설정
        #     if p is None and q is None: # 더 이상 탐색 대상 없음 -> 종료 (True)
        #         return True

        #     if p is None or q is None: # 둘이 값이 다름 -> 종료 (False)
        #         return False 
        #     if p.val != q.val: 
        #         return False
            
        #     return _recur(p.left, q.left) and _recur(p.right, q.right)

        # return _recur(p, q)