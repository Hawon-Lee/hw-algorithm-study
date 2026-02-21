def solution(answers):
    patterns = [
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]
    ]
    score_ls = []
    result = []
    
    for pattern in patterns:
        curr_score = 0
        for i, ans in enumerate(answers):
            if ans == pattern[i % len(pattern)]:
                curr_score += 1
        score_ls.append(curr_score)
    
    max_score = max(score_ls)
    for i, s in enumerate(score_ls):
        if s == max_score:
            result.append(i+1)
            
    return result
