# https://leetcode.com/problems/maximum-depth-of-binary-tree/

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:

        def _recur(node, curr_depth, depth_ls=[]):
            # 재귀 종료 조건
            if node is None:
                depth_ls.append(curr_depth)
                return depth_ls
            curr_depth += 1

            # 탐색
            depth_ls = _recur(node.left, curr_depth, depth_ls)
            depth_ls = _recur(node.right, curr_depth, depth_ls)
            return depth_ls

        depth_ls = _recur(root, 0, [])
        
        return max(depth_ls)