import re
# import modular2 as f

# c = '[1;2;3],[1;4;18],[4;2;18],[1;;5]'
# match_r_sist = re.findall(r"\[(-?\d+);(-?\d+);(-?\d+)\]", c)
# lista_argus = list(map(list, zip(*(map(int,num) for num in match_r_sist))))
# print(lista_argus)

n = 61
lista = list(range(2,n-1))
for i in range(2, int(n**0.5+1)):
    for j in range(i+1, lista[-1]):
        if j%i == 0: 
            lista = lista[:j-1]+ lista[j:]
    print(lista)


# lista = [1,2,3,4,5,6,7,8,9]
# j = 5
# lista = lista[:j-1]+ lista[j:]
# print(lista)