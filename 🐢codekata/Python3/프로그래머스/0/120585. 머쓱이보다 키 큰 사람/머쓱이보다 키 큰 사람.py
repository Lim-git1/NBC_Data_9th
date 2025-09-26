def solution(array, height):
    cnt = 0
    for i in array:
        if height < i :
            cnt += 1
    answer = cnt
    return answer