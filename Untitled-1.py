import re
import modular as f

# c = '[1;2;3],[1;4;18],[4;2;18],[1;;5]'
# match_r_sist = re.findall(r"\[(-?\d+);(-?\d+);(-?\d+)\]", c)
# lista_argus = list(map(list, zip(*(map(int,num) for num in match_r_sist))))
# print(lista_argus)

b = 1
a = 11
lista = list(range(2,b))
result = list(range(max(a,2),b))
print(result)
i = lista[0]
while i <= (lista[-1])**0.5:
    for j in lista[lista.index(i)+1:]: 
        if j%i == 0: 
            lista = lista[:lista.index(j)] + lista[lista.index(j)+1:]
            if j in result: 
                result = result[:result.index(j)] + result[result.index(j)+1:]
    i = lista[lista.index(i)+1]
print(result)


# lista = [1,2,3,4,5,6,7,8,9]
# j = 5
# lista = lista[:j-1]+ lista[j:]
# print(lista)

# def bla(a, b): 
#     if a >= b: 
#         return []
#     lista = list(range(a,b+1))
#     while not f.es_primo(a):
#         lista[1:]
#         a = lista[0]
#     if lista == []: 
#         return []
#     i = 2
#     while i < lista[-1]:
#         for j in lista[lista.index(i)+1:]: 
#             if j%i == 0: 
#                 lista = lista[:lista.index(j)] + lista[lista.index(j)+1:]
#         print(lista)
#         i = lista[lista.index(i)+1]
#     return lista

# if __name__ == '__main__': 
#     print(bla(5,10))