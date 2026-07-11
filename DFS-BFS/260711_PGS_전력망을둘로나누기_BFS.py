# https://school.programmers.co.kr/learn/courses/30/lessons/86971

from collections import deque
def solution(n, wires):
    # 연결 하나씩 빼보면서 두 그룹의 BFS 총 길이 비교

    def get_adj(wires):
        adj = {}
        for start, end in wires:
            if start not in adj:
                adj[start] = []
            if end not in adj:
                adj[end] = []
            adj[start].append(end)
            adj[end].append(start)
        return adj
                
    def get_search(start, adj):
        queue = deque([start])
        visited = {start}
        while queue:
            curr_node = queue.popleft()
            nb_node_ls = adj.get(curr_node, [])
            for nb in nb_node_ls:
                if nb not in visited:
                    queue.append(nb)
                    visited.add(nb)
            
        return visited
    
    # main
    answer = float("inf")
    for i in range(len(wires)): # wire index 로 접근
        curr_wires = wires[i]
        remain_wires = wires[:i] + wires[i+1:]
        adj = get_adj(remain_wires)
        group_1 = get_search(curr_wires[0], adj)
        group_2 = get_search(curr_wires[-1], adj)
        diff_size = abs(len(group_1)-len(group_2))
        if diff_size < answer:
            answer = diff_size

    return answer