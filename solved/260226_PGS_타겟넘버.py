def solution(numbers, target):
    answer = 0
    
    def _dfs(curr_depth, curr_sum):
        nonlocal answer
        if curr_depth == len(numbers):
            if curr_sum == target:
                answer += 1
            return
        _dfs(curr_depth + 1, curr_sum + numbers[curr_depth])
        _dfs(curr_depth + 1, curr_sum - numbers[curr_depth])
        
    _dfs(0, 0)
    return answer
