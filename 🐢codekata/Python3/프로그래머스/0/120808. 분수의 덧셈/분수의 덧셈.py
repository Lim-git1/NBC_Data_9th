def gcd(a, b):
    while b>0:
        a, b = b, a%b
    return a

def solution(numer1, denom1, numer2, denom2):
    j = numer1*denom2 + numer2*denom1
    m = denom1*denom2
    g = gcd(j, m)
    answer = [j//g, m//g]
    return answer