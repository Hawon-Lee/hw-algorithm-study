class Solution:
    def rob(self, nums: List[int]) -> int:
        # # [Top-down]
        # sum_per_pos = {}
        # def helper(given_nums):
        #     curr_pos = len(nums) - len(given_nums) # 현재 포인터 위치

        #     # 현재 포인터 위치의 sum값이 이미 존재하는지 확인
        #     if curr_pos in sum_per_pos:
        #         return sum_per_pos[curr_pos]
            
        #     # 재귀 반환 조건 -> 남은 길이가 2 이하인 경우
        #     if len(given_nums) <= 2: # 뒤에서 1 or 2번째 위치인 경우
        #         sum_per_pos[len(nums)-len(given_nums)] = max(given_nums)
        #         return max(given_nums)

        #     v1 = helper(given_nums[1:]) # 첫번째 값을 선택하지 않음
        #     v2 = given_nums[0] + helper(given_nums[2:]) # 첫번째 값을 선택함
        #     sum_per_pos[curr_pos] = max(v1, v2)
        #     return max(v1, v2)

        # return helper(nums)

########################################################################

        # [bottom-up]
        # if len(nums) <= 1:
        #     return max(nums) if nums else 0
        # dp = [0] * len(nums)
        # dp[0] = nums[0]
        # dp[1] = max(nums[0], nums[1])
        # for i in range(len(nums)-2):
        #     dp[i+2] = max(dp[i] + nums[i+2], dp[i+1])
        # return dp[-1]

        # [bottom-up w/ 공간최적화]
        if len(nums) <= 1:
            return max(nums) if nums else 0
        
        # dp initialization
        prev1, prev2 = max(nums[0], nums[1]), nums[0]
        for i in range(2, len(nums)):
            prev1, prev2 = max(prev1, prev2+nums[i]), prev1

        return max(prev2, prev1)