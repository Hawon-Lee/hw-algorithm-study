def solution(n, costs):
# idea 1: 모든 조합별 코스트 비교 -> 그렇다면 완전 연결을 어떻게 판별? (기각)
# idea 2: 값 낮은 에지부터 연결, 단 이미 같은 그룹인 섬을 또 연결하는 그룹은 패스 (채택)

    sorted_costs = sorted(costs, key=lambda x: x[-1])
    parent = [i for i in range(n)]
    
    def find(x):
        if parent[x] != x:
            return find(parent[x])
        else:
            return x
    answer = 0
    for n1, n2, cost in sorted_costs:
        n1 = find(n1) # find root node
        n2 = find(n2)
        if n1 == n2: # two nodes alread in same group
            continue
        if n1 < n2:
            parent[n2] = n1
        else:
            parent[n1] = n2
        answer += cost        
            
    return answer