# 기존 풀이
'''
def solution(n, computers):
    answer = 0
    node_ls = list(range(n))
    to_visit, visited = [0], []

    while to_visit:
        curr_node = to_visit.pop()
        visited.append(curr_node)
        to_visit.extend([i for i in range(n) if i not in visited and computers[curr_node][i] == 1])

        if to_visit == []:
            answer += 1
            remain_nodes = [node for node in node_ls if node not in visited]
            if not remain_nodes:
                break
            to_visit.append(remain_nodes[0])

    return answer
'''

# 피드백 버전 (list->set for 빠른 탐색)
def solution(n, computers):
    answer = 0
    to_visit, visited = [0], set()
    
    while to_visit:
        curr_node = to_visit.pop()
        visited.add(curr_node)
        to_visit.extend([i for i in range(n) if i not in visited and computers[curr_node][i] == 1])
        
        if not to_visit:
            answer += 1
            remain_nodes = [node for node in range(n) if node not in visited]
            if not remain_nodes:
                break
            to_visit.append(remain_nodes[0])
            
    return answer
