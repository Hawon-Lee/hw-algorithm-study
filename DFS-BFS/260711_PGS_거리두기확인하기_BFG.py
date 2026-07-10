# https://school.programmers.co.kr/learn/courses/30/lessons/81302

from collections import deque
def solution(places):
    class Explorer:
        def get_neighbor(self, pos: tuple):
            nb_ls = []
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                dst = (pos[0]+dr, pos[1]+dc)

                if dst in self.visited:
                    continue

                if not (
                    (0 <= dst[0] < len(place)) and (0 <= dst[1] < len(place[0]))
                ):
                    continue

                if place[dst[0]][dst[1]] == "X": # 없어도 되지만 명시적으로.
                    continue

                if place[dst[0]][dst[1]] == "P":
                    print(pos, dst[0], dst[1], self.visited)
                    return -1 # 종료 시그널

                self.visited.add(dst)
                nb_ls.append(dst)
            return nb_ls


        def supervise(self, place):
            # place 예시: ["POOOP", "OXXOX", "OPXPX", "OOXOX", "POXXP"]
            for ir, row in enumerate(place):
                for ic, col in enumerate(row):
                    if col == "P":
                        curr_pos = (ir, ic)
                        self.visited = set()
                        self.visited.add((ir, ic))
                        nb_ls = self.get_neighbor(curr_pos)
                        if nb_ls == -1:
                            return 0
                        for pos in nb_ls: # 두 번째 탐색
                            nb_ls = self.get_neighbor(pos)
                            if nb_ls == -1:
                                return 0
            return 1

    Ex = Explorer()
    answer = []
    for place in places:
        is_ok = Ex.supervise(place)
        answer.append(is_ok)
        
    return answer