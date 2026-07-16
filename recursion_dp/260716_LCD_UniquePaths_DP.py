class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # # [top-down: m,n 에 도달하는 경우의 수는 m-1, n 이랑 m, n-1 에 도달하는 경우의 수를 더한다]
        # memo = {}

        # def helper(m, n, memo):
        #     if m == 1 or n == 1:
        #         return 1
        #     if (m, n) in memo:
        #         return memo[(m, n)]
        #     memo[(m, n)] = helper(m-1, n, memo) + helper(m, n-1, memo)
        #     return memo[(m, n)]
        
        # return helper(m, n, memo)
        
############################################################################################

        # [bottom-up: m-1, n 과 m, n-1 에 도달한 경우의 수를 더해서 m, n 을 계산한다]
        array = [n * [0] for _ in range(m)]

        for row in range(0, m):                
            for col in range(0, n):
                if row == 0 or col == 0:
                    array[row][col] = 1
                    continue # continue 없으면 row = 0 일때 밑에서 array[-1] 이 되어버림
                array[row][col] = array[row-1][col] + array[row][col-1]
        return array[m-1][n-1]
