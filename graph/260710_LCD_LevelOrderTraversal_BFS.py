# https://leetcode.com/problems/binary-tree-level-order-traversal/

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        queue = deque([root])
        visited = []
        output = []

        while queue:
            level_size = len(queue)
            level_vals = []
            for _ in range(level_size):
                curr_node = queue.popleft()
                level_vals.append(curr_node.val)
                if curr_node.left:
                    queue.append(curr_node.left)
                if curr_node.right:
                    queue.append(curr_node.right)
            output.append(level_vals)
            level_vals = []

        return output