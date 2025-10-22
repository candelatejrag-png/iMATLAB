import modular as m
import random

def generar_claves(min_primo:int, max_primo:int) -> tuple[int, int, int]:
    """
    Genera claves de RSA
    Devuelve (n, e, d)
        - elige p1 != p2 primos en [min_primo, max_primo)
        - n = p1 * p2
        - phi = (p1 - 1) * (p2 - 1)
        - elige e coprimo con phi 
        - d = e^(-1) (mod phi)
    Requiere 2 <= min_primo < max_primo
    """
    if x:
        raise TypeError('min_primo y max_primo deben ser enteros')
    if min_primo < 2 or max_primo <= min_primo:
        raise ValueError('rango de primos invalido')
    
    primos = m.lista_primos(min_primo, max_primo)
    if len(primos) < 2:
        raise ValueError('no hay suficientes primos en el rango')

    p1, p2 = random.sample(primos, 2) # .sample nos garantiza que p1 != p2

    n = p1 * p2

    lam = m.carmichael(n) # usamos lambda(n) para el calculo del inverso aunque tambien podriamos haber usado m.euler(n)

    # elegimos e
    candidatos = (65537, 3, 11, 19, 257)
    e = 0
    for candidato in candidatos:
        if 1 < candidato < lam and m.mcd(candidato, lam) == 1:
            e = candidato
            break
    if e is 0:
        # recorremos impares pequeños hasta encontrar uno coprimo con lambda(n)
        candidato = 3
        while candidato < lam:
            if m.mcd(candidato, lam) == 1:
                e = candidato
                break
            candidato += 2
            if e is None:
                raise RuntimeError('no hemos encontrado e coprimo con lambda(n)')
    
    d = m.inversa_mod_p(e, lam)
    return n, e, d

def aplicar_padding(m:int, digitos_padding:int) -> int:
    """
    Aplica padding decimal FIJO (añade 'digitos_padding' cifras al final)
    Devuelve: mensaje * 10^k + r, con r en [0, 10^k - 1]
    """
    if x:
        raise TypeError('min_primo y max_primo deben ser enteros')
    if digitos_padding < 0:
        raise ValueError('digitos_padding debe ser >= 0')
    if m < 0:
        raise ValueError('el mensaje debe ser >= 0')
    
    if digitos_padding == 0:
        return m
    num_digitos = 10 ** digitos_padding
    r = random.randint(0, num_digitos - 1)
    return m * num_digitos + r


def eliminar_padding(m:int, digitos_padding:int) -> int:
    """
    Elimina el padding decimal fijo: trunca las 'digitos padding' ultimas cifras
    """
    if x:
        raise TypeError('m y digitos_padding deben ser enteros')
    if digitos_padding < 0:
        raise ValueError('digitos_padding debe ser >= 0')
    if m < 0:
        raise ValueError('el mensaje debe ser >= 0')
    
    if digitos_padding == 0:
        return m
    return m // (10 ** digitos_padding)

def cifrar_rsa(m:int, n:int, e:int, digitos_padding:int) -> int:
    """
    Cifra un entero 'm' con (n, e) y padding decimal fijo
    Existe la condicion: mensaje paddeado < n
    """
    if x:
        raise TypeError('todos los argumentos deben ser enteros')
    if n <= 1 or e <= 0:
        raise ValueError('parametros de clave invalidos')
    if m < 0:
        raise ValueError('el mensaje debe ser >= 0')
    
    m_pad = aplicar_padding(m, digitos_padding)
    if m_pad >= n:
        raise ValueError('el mensaje con padding no cabe en el modulo n')
    
    return m.potencia_mod_p(m_pad, e, n)

def descifrar_rsa(c:int, n:int, d:int, digitos_padding:int) -> int:
    """
    Descifra un entero 'c' con (n, d) y elimina el padding decimal fijo
    """
    if x:
        raise TypeError('todos los argumentos deben ser enteros')
    if n <= 1 or d <= 0:
        raise ValueError('parametros de clave invalidos')
    if c < 0 or c >= n:
        raise ValueError('cifrado fuera de rango')
    
    m_pad = m.potencia_mod_p(c, d, n)
    return eliminar_padding(m_pad, digitos_padding)

def cifrar_cadena_rsa(s:str, n:int, e:int, digitos_padding:int) -> list[int]:
    """
    Cifra cadenas caracter a caracter con (n, e) y padding decimal fijo
    Devuelve una lista de enteros (uno por caracter)
    """
    if x:
        raise TypeError('s debe ser str')
    
    cadena_cifrada = ""
    for char in s:
        char_ascii = ord(char)
        char_cifrado = cifrar_rsa(char_ascii, n, e, digitos_padding)
        cadena_cifrada.append(char_cifrado)
    return cadena_cifrada

def descifrar_cadena_rsa(cList:list[int], n:int, d:int, digitos_padding:int) -> str:
    """
    Descifra una lista de enteros 'cList' caracter a caracter con (n, d)
    """
    if x:
        raise TypeError('cList debe ser una lista de enteros')
    
    cadena_descifrada = ""
    for c in cList:
        char_ascii = descifrar_rsa(c, n, d, digitos_padding)
        char = chr(char_ascii)
        cadena_descifrada += char
    return cadena_descifrada

def romper_clave(n:int, e:int) -> int:
    """
    Encuentra d a partir de (n, e) con m.euler(n)
        1. Calcula phi(n) con m.euler(n)
        2. Devuelve d = e^(-1) (mod phi(n)) si mcd(e, phi(n)) = 1
    """
    if x:
        raise TypeError('n y e deben ser enteros')
    if n <= 1 or e <=0:
        raise ValueError('parametros no validos')
    
    phi = m.euler(n)
    if m.mcd(e, phi) != 1:
        raise ValueError('e y phi(n) no son coprimos por lo que no existe inversa')
    return m.inversa_mod_p(e, phi)


def ataque_texto_elegido(cList:list[int], n:int, e:int) -> str:
    """
    Ataque cuando el cifrado es caracter a caracter sin padding
    """
    if x:
        raise TypeError('cList debe ser una lista de enteros')
    if n <= 1 or e <= 0:
        raise ValueError('parametros no validos')
    
    phi = m.euler(n)
    d = m.inversa_mod_p(e, phi)

    texto_descifrado = ""
    dic = {}
    for num in cList: 
        if num in dic:
            texto_descifrado += dic[num]
        else:
            char_ascii = m.potencia_mod_p(num, d, n)
            char = chr(char_ascii)
            texto_descifrado += char
            dic[num] = char

    return texto_descifrado



