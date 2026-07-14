# https://leetcode.com/problems/redundant-connection/description/

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent = list(range(0, n+1)) # [0, 1, 2, 3, 4, ...

        def find(x):
            if parent[x] != x:
                return find(parent[x])
            else:
                return x
                    
        for n1, n2 in edges:
            n1_orig, n2_orig = n1, n2
            n1 = find(n1)
            n2 = find(n2)
            if n1 == n2:
                return [n1_orig, n2_orig]
            if n1 < n2:
                parent[n2] = n1
            elif n1 >= n2:
                parent[n1] = n2