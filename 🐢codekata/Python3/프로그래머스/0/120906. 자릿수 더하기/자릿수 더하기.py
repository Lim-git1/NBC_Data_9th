def solution(n):
    sum=0
    while n>0 :
        k = n%10
        sum = sum + k
        n = n//10

    return sum