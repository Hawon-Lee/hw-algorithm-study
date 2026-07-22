# https://leetcode.com/problems/longest-common-subsequence/description/

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # text 1 이 항상 짧도록 보증
        if len(text1) > len(text2):
            text1, text2 = text2, text1
        
        dp = [[0] * len(text2) for _ in range(len(text1))]

        for i in range(len(text1)):
            for j in range(len(text2)):
                if i == 0:
                    dp[0][j] = 1 if text1[0] in text2[:j+1] else 0
                    continue
                if j == 0:
                    dp[i][0] = 1 if text2[0] in text1[:i+1] else 0
                    continue
                if text1[i] == text2[j]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        return dp[len(text1)-1][len(text2)-1]