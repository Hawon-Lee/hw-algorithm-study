from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        init_fresh_cnt = 0 # 초기 신선한 오렌지 수, 탐색 완료 후에 갯수 남으면 -1 반환
        max_t = 0 # BFS로 탐색한 최대 횟수 (깊이))
        queue = deque()
        visited_ls = set()

        for ir, r in enumerate(grid):
            for ic, c in enumerate(r):
                if c == 1:
                    init_fresh_cnt += 1
                if c == 2:
                    queue.append((ir, ic, 0))
        
        def get_nb_orange(pos: tuple[int, int, int]) -> list:
            nonlocal max_t
            nb_orange_ls = []
            curr_r = pos[0]
            curr_c = pos[1]
            curr_t = pos[2]

            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                moved_pos = (curr_r + dr, curr_c + dc)
                if moved_pos in visited_ls:
                    continue
                if not (
                    (0 <= moved_pos[0] < len(grid)) and 0 <= moved_pos[1] < len(grid[0])
                    ):
                    continue
                if grid[moved_pos[0]][moved_pos[1]] == 1:
                    nb_orange_ls.append(
                        (moved_pos[0], moved_pos[1], curr_t+1) # (x+dr, y+dc, t+1)
                    ) 
                    visited_ls.add(moved_pos)
                    max_t = max(curr_t+1, max_t)
            return nb_orange_ls
                    
        while queue:
            curr_pos = queue.popleft()
            nb_orange = get_nb_orange(curr_pos) # [(x+dr, y+dc, t+1), ...]
            queue += nb_orange

        if init_fresh_cnt != len(visited_ls): # 탐색 후에도 신선 오렌지가 여전히 남아있다면
            return -1

        return max_t