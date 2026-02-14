def solution(participant, completion):
#     # 1번 풀이: sorting/loop -> 32.65ms / 17MB
#     participant.sort()
#     completion.sort()
#     for i in range(len(completion)):
#         if participant[i] != completion[i]:
#             return participant[i]
#     return participant[-1]


#     # 2번 풀이: hash -> 23.72ms / 23MB
#     hash_dict = {}
#     sum_hash = 0
#     for part in participant:
#         hash_dict[hash(part)] = part
#         sum_hash += hash(part)
#     for comp in completion:
#         sum_hash -= hash(comp)
#     return hash_dict[sum_hash]


#     # 3번 풀이: Counter -> 39.42ms / 23.4MB
#     from collections import Counter
#     part_counter = Counter(participant)
#     comp_counter = Counter(completion)
#     difference = part_counter - comp_counter
#     return list(difference.keys())[0]