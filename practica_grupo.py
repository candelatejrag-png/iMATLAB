# Mesa B

import modular as m 

# numeros primos escogidos
p1 = 998813
p2 = 981011

# módulo
n = p1 * p2     # 979846539943

# phi(n)
phi = (p1 - 1) * (p2 - 1)

# clave pública
e = 19

# d = e^(-1) (mod phi)
d = m.potencia_mod_p(e, -1, phi) 
print(f'\nClaves de la mesa B para RSA: ')
print(f'Clave privada: {d}')  # 464136896899  

# candado = ne
print(f'Clave pública: {n} {e}')

# enviamos mensaje cifrado a grupo C
numero = 1113
n_mesa_C =  747872501029
e_mesa_C = 74787251029
cifrado = m.potencia_mod_p(numero, e_mesa_C, n_mesa_C)  # mensaje^e (mod n), con su e y n
print(f'\nEl mensaje {numero} cifrado con la clave del grupo C es {cifrado}')

# desciframos el mensaje que nos ha llegado del grupo A
numero_cifrado = 292754272551
numero_descifrado = m.potencia_mod_p(292754272551, d, n)   # mensaje^d (mod n)
print(f'\nLa mesa A nos ha mandado {numero_cifrado} como mensaje cifrado, lo desciframos y nos da el número {numero_descifrado}')

# enviamos texto cifrado a grupo A
texto = 'clase'
n_mesa_A =  995336518789
e_mesa_A = 11
mensaje_cifrado = []
for char in texto:
    char_ascii = ord(char)
    char_cifrado = m.potencia_mod_p(char_ascii, e_mesa_A, n_mesa_A)
    mensaje_cifrado.append(char_cifrado)
print(f"\nLa palabra '{texto}' cifrada con la clave de la mesa A es: ")
for num in mensaje_cifrado:
    print(num, end = " ")

# desciframos el texto que nos ha llegado del grupo C
texto_cifrado = [385106506114, 42950339179, 880508418327, 545875393369, 557815054846]
texto = ""
for num in texto_cifrado:
    char_ascii = m.potencia_mod_p(num, d, n)
    char = chr(char_ascii)
    texto += char
print(f"\n\nLa mesa C nos ha mandado la palabra '{texto}' cifrada")

# rompemos la clave privada de la mesa A
phi_mesa_A = m.euler(n_mesa_A)
d_mesa_A = m.inversa_mod_p(e_mesa_A, phi_mesa_A)
print(f'\nHemos roto la clave RSA de la mesa A. Su d es {d_mesa_A}')

# desciframos el mensaje de X
import re
n_X = 28282590191348679547
e_X = 15780653617344828671

# Inicialmente se quiso romper la clave empleando la funcion de euler con el código siguiente: 
# phi_X = m.euler(n_X)
# Sin embargo este código tardó algo de tiempo en ejecutarse, por lo que se decidió emplear otro enfoque utilizando el siguiente código: 
p,q = m.factorizar_cripto(28282590191348679547)
phi_X = (p-1)*(q-1)
# Este este rompe la clave de X en cuestión de pocos segundos. 

d_X = m.inversa_mod_p(e_X, phi_X)

with open('criptograma_X.txt', 'r', encoding = 'utf-8') as f:
    for i in range(3):
        f.readline()
    texto_X = f.readline().strip()

nums = []
coincidencias = re.findall(r'\d+', texto_X)
for n in coincidencias:
    numero = int(n)
    nums.append(numero)

texto_descifrado = "" 
dic = {}
for num in nums: 
    if num in dic:
        texto_descifrado += dic[num]
    else:
        char_ascii = m.potencia_mod_p(num, d_X, n_X)
        char = chr(char_ascii)
        texto_descifrado += char
        dic[num] = char

print(f'\nEl texto descifrado de X es: ')
print(texto_descifrado)

print(f'\nEste texto es un fragmento de la obra El fractal, escrito por Susana Merchán')