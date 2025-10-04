import re
import modular as f

# c = '[1;2;3],[1;4;18],[4;2;18],[1;;5]'
# match_r_sist = re.findall(r"\[(-?\d+);(-?\d+);(-?\d+)\]", c)
# lista_argus = list(map(list, zip(*(map(int,num) for num in match_r_sist))))
# print(lista_argus)

b = 61
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







# # 14
# def ec_cuadratica(a:int, b:int, c:int, p:int):
#     """
#     Devuelve las dos raices (posiblemente iguales) de ax^2 + bx + c = 0 (mod p) con p primo
#         - si no hay raices: devuelve None
#         - si hay dos raices: (x1, x2) con x1 < x2
#         - si hay una doble: (x, x)
#     Casos como a = 0 (mod p) se tratan como ecuacion lineal
#     """
#     if p <= 1 or not es_primo(p):
#         raise ValueError("p debe ser primo")
#     a %= p
#     b %= p
#     c %= p

#     if a == 0:
#         # bx + c = 0 (mod p)
#         if b == 0:
#             if c == 0:
#                 # infinitas soluciones -> por convencion devolvemos (0,0)
#                 return (0, 0)
#             else:
#                 return None
#         x = (-c * inversa_mod_p(b, p)) % p
#         return (x, x)
    
#     # discriminante
#     delta = (b*b -4*a*c) % p
#     r = raiz_mod_p


# # 12. (Opcional) Expandir la funcionalidad de resolver sistema congruencias y del comando resolverSistema para
# # resolver sistemas de ecuaciones donde los m´odulos no son coprimos entre s´ı.
# # 13. (Opcional) Investigar el algoritmo de Cipolla y programar en “modular.py” una funci´on
# # raiz mod p(n : int, p : int) −→ int
# # que reciba un entero n y un n´umero primo p y calcule una ra´ız de n m´odulo p, es decir, un entero x tal que
# # x
# # 2 ≡ n (mod p)
# # Usando dicha funci´on, agregar a IMAT-LAB un comando
# # raiz(n, p)
# # que devuelva lo siguiente:
# #  Si n tiene dos ra´ıces distintas x1 < x2, las escribe en orden: “x1, x2”
# #  Si n tiene una ´unica ra´ız x, escribe “x”
# #  Si n no tiene ra´ıces, como con el resto de comandos, escribe “NE” en modo “batch” o un mensaje de error
# # adecuado en modo interactivo.
# # 14. (Opcional) Usando la funci´on anterior, implementar en “modular.py” una funci´on
# # ecuacion cuadratica(a : int, b : int, c : int, p : int) −→ T uple[int, int]
# # que reciba enteros a, b, c y p, con p n´umero primo, y devuelva las dos soluciones m´odulo p (posiblemente repetidas)
# # de la ecuaci´on
# # ax2 + bx + c ≡ 0 (mod p)
# # Usando dicha funci´on, agregar a IMAT-LAB un comando
# # ecCuadratica(a, b, c, p)
# # que implemente la funcionalidad anterior y devuelva lo siguiente
# #  Si la ecuaci´on tiene dos ra´ıces distintas x1 < x2, las escribe en orden: “x1, x2”
# #  Si la ecuaci´on tiene una ´unica ra´ız doble x, escribe “x”
# #  Si la ecuaci´on no tiene ra´ıces, como co









