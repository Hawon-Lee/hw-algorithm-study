# https://leetcode.com/problems/flood-fill/

class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        to_visit_ls = [(sr, sc)]
        visited_ls = set()
        visited_ls.add((sr, sc))
        init_color = image[sr][sc]
        
        if init_color == color:
            return image

        # helper function
        def get_same_neighbors(sr, sc):
            same_nb_ls = []

            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                dst = (sr+dr, sc+dc)
                
                # 범위를 벗어난 도착점은 제거
                if not (
                    (0 <= dst[0] < len(image)) and (0 <= dst[1] < len(image[0]))
                ):
                    continue
                
                # 이미 방문한 점도 제거
                if dst in visited_ls:
                    continue

                # 색상이 같은 도착점을 추가
                if image[dst[0]][dst[1]] == init_color:
                    same_nb_ls.append(dst)
                    visited_ls.add(dst)

            return same_nb_ls

        # dfs
        while to_visit_ls:
            curr_pos = to_visit_ls.pop(-1)
            same_nb_ls = get_same_neighbors(curr_pos[0], curr_pos[1])
            to_visit_ls += same_nb_ls
        
        # 방문 장소 색칠 후 반환
        for (vr, vc) in visited_ls:
            image[vr][vc] = color

        return image