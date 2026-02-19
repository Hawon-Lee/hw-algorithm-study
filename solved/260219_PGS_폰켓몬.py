def solution(nums):
    nums_to_sele = len(nums) / 2
    uniq_nums = list(set(nums))
    
    if nums_to_sele > len(uniq_nums):
        return len(uniq_nums)
    else:
        return nums_to_sele