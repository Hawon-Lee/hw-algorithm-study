# https://leetcode.com/problems/binary-tree-inorder-traversal/

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        rst = []
        return self._recur(root, rst)

    def _recur(self, curr_pos, rst):
        if curr_pos is None:
            return []
        self._recur(curr_pos.left, rst)
        rst.append(curr_pos.val)
        self._recur(curr_pos.right, rst)

        return rst