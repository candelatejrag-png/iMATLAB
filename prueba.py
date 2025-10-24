def criba(N):
    es_primo = [True] * (N + 1)
    es_primo[0] = es_primo[1] = False
    p = 2
    while p * p <= N:
        if es_primo[p]:
            for multiple in range(p*p, N+1, p):
                es_primo[multiple] = False
        p += 1
    return es_primo