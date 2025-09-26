# def solution(n, numlist):
#     for i in numlist:
#         if i % n != 0:
#             numlist.remove(i)

#     return numlist

def solution(n, numlist):
    new_list = []
    for i in numlist:
        if i % n == 0:
            new_list.append(i)

    return new_list