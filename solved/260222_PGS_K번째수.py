def solution(array, commands):
    answer = []
    for i, j, k in commands:
        target = array[i-1:j]
        target.sort()
        answer.append(target[k-1])
    
    return answer
