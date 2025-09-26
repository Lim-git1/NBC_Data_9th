def solution(n):
    sqrt = n ** (1/2)

    return 2 if sqrt%1 != 0 else 1
