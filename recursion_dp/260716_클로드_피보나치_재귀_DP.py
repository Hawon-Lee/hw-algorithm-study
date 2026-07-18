# 문제: 피보나치 수열의 n번째값 반환 (0, 1, 1, 2, 3, 5, 8, 13, ...)

# Recursion
def fib_rc(n): 
    if n <= 1:
        return n
    return fib_rc(n-1) + fib_rc(n-2) # 느리다. 왜? 왼쪽/오른쪽 항이 각각 별도로 재귀를 실행

# DP
def fib_dp(n, memo={}):
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib_dp(n-1, memo) + fib_dp(n-2, memo)
    return memo[n]