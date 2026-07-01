# https://school.programmers.co.kr/learn/courses/30/lessons/1844?language=python3

def solution(maps):
    visited_ls = set() # set 의 in 검사 -> 빠름. (list in 검사는 O(N))

    def _get_dst_ls(curr_pos, curr_depth, maps, visited_ls):
        """실제로 갈 수 있는 방향의 튜플만 리스트로 제공"""
        dst_ls = []
        
        # 4방향 튜플
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dst = (curr_pos[0]+dr, curr_pos[1]+dc)
            # visited node 는 드랍
            if dst in visited_ls:
                continue
            # 경계 검사용 컨디션 (경계 넘으면 True)
            if not (
                (1 <= dst[0] <= len(maps)) and (1 <= dst[1] <= len(maps[0]))
            ):
                continue
            
            # 남은 노드중 길인 곳만 추가 (순서 위로 올리면 indexing error)
            if maps[dst[0]-1][dst[1]-1] == 1:
                dst_ls.append((dst, curr_depth + 1))
                visited_ls.add(dst)
        return dst_ls

    curr_pos = (1, 1)
    curr_depth = 1
    
    to_visit_ls = [(curr_pos, curr_depth)]
    
    while to_visit_ls:
        curr_pos, curr_depth = to_visit_ls.pop(0) # BFS
        dst_ls = _get_dst_ls(curr_pos, curr_depth, maps, visited_ls) # 갈 수 있는 (위치, 깊이) 리스트
        
        # 도달시 현재 깊이 반환
        if curr_pos == (len(maps), len(maps[0])):
            return curr_depth
        
        # Queue 추가
        to_visit_ls += dst_ls
    
    return -1