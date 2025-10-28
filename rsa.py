"""
rsa.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP10
Integrantes:
    - Candela Tejedo Raga
    - Gabriela Romero Martín

Descripción:
Librería para la realización de cifrado y descifrado usando el algoritmo RSA.
"""
import modular as f
from typing import Tuple,List
import random


def generar_claves(min_primo:int,max_primo:int)-> Tuple[int,int,int]:
    """
    Toma dos primos entre min_primo (incluido) y max_primo (excluido) y devuelve
    n,e,d
    donde (n,e) es la clave pública y d la clave privada para RSA

    Args:
        min_primo (int): Límite inferior para los primo p1 y p2 usados en la clave
        max_primo (int): Límite superior para los primo p1 y p2 usados en la clave
    
    Returns:
        n (int): Módulo para RSA, formado por el producto de dos primos p1 y p2 tales que
            min_primo<=p1, p2 < max_primo
        e (int): Exponente de la clave pública para RSA con módulo n=p1*p2
        d (int): Exponente de la clave privada para RSA con módulo n

    Raises:
        ValueError: Si no es posible encontrar una pareja de primos distintos p1,p2 entre min_primo y max_primo
    """
    if min_primo < 2 or max_primo <= min_primo:
        raise ValueError('rango de primos invalido')
    
    primos = f.lista_primos(min_primo, max_primo)
    if len(primos) < 2:
        raise ValueError('no hay suficientes primos en el rango')

    p1, p2 = random.sample(primos, 2) # en vez de usar random.choice() y luego un while, random.sample(poblacon, k) devuelve una lista de k elementos DISTINTOS de la poblacion en orden aleatorio
    
    n = p1 * p2

    # elige e al azar con condiciones: 1 < e < m.euler(n), e impar, mcd(e, m.euler(n))=1
    phi = (p1 - 1) * (p2 - 1)

    # elegimos e
    if phi <= 3:
        if phi == 2:
            raise RuntimeError('no existe exponente valido para phi(n)= 2')
        e = 2   # si phi = 3
    else:
        probados = set() #no podemos contar intentos porque random.randrange puede repetir valores por lo que podria raise el error sin haber probado todos los impares
        n_candidatos = len(range(3, phi,2))
        while True: # intenta hasta encontrar un e valido
            e = random.randrange(3, phi, 2) # devuelve un numero aleatorio en [3, phi) ,2 para que pruebe solo e impares
            probados.add(e)
            if f.mcd(e, phi) == 1:
                break
            if len(probados) == n_candidatos:
                raise RuntimeError('no hemos encontrado e coprimo con phi(n)')

    d = f.inversa_mod_p(e, phi)
    return n, e, d


def aplicar_padding(m:int,digitos_padding:int) -> int:
    """Dado un mensaje y un número de dígitos de padding, añade
    digitos_padding cifras aleatorias a la derecha del mensaje
    
    Args:
        m (int): Mensaje sin padding
        digitos_padding (int): Número no negativo de cifras de padding
    
    Returns:
        int: entero formado por los dígitos de m seguidos de digitos_padding cifras aleatorias.

    Raises: None

    Example:
        aplicar_padding(24,2)=2419
        aplicar_padding(24,2)=2403
        aplicar_padding(24,3)=24718
        aplicar_padding(24,3)=24845
        aplicar_padding(24,0)=24
    """
    # asumimos que m >= 0 y digitos_padding >= 0 son precondiciones del comentario por Raises: None
    if digitos_padding == 0:
        return m
    factor = 10 ** digitos_padding
    r = random.randint(0, factor - 1) # genera un bloque aleatorio de 'digitos_padding' cifras 
    return m * factor + r   # se desplaza el mensaje por el factor y se le añade el bloque aleatorio


def eliminar_padding(m:int,digitos_padding:int)->int:
    """Dado un mensaje con padding de digitos_padding cifras al
    final del mismo, elimina dichas cifras aleatorias y devuelve
    el resto de cifras del mensaje

    Args:
        m (int): Mensaje con padding
        digitos_padding (int): Número no negativo de cifras de padding
    
    Returns:
        int: entero resultante de eliminar las últimas digitos_padding cifras de m.

    Raises: None
    
    Example:
        eliminar_padding(2454,1)=245
        eliminar_padding(2454,2)=24
        eliminar_padding(2454,3)=2
        eliminar_padding(2432,2)=24
        eliminar_padding(2432,0)=2432
    """
    if digitos_padding == 0:  # no hay cifras que eliminar
        return m
    factor = 10 ** digitos_padding
    return m // factor # trunca las 'factor' cifras finales

def cifrar_rsa(m:int,n:int,e:int,digitos_padding:int)->int:
    """Dado un mensaje m entero, un módulo y exponente que formen parte
    de una clave pública de RSA, con m<n*10^{-digitos_padding}, y un número
    de dígitos de padding, aplica el padding al mensaje y lo cifra
    usando RSA con módulo n y exponente e.
    
    Args:
        m (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA
        e (int): Exponente de la clave pública de RSA
        digitos_padding (int): Número no negativo de cifras de padding
    
    Returns:
        int: entero resultante de agregar el padding a m y aplicar RSA.

    Raises: None
    """
    # asumimos que m_pad < n asi que no cazamos error?
    m_pad = aplicar_padding(m, digitos_padding) # primero concatenamos las cifras aleatorias a la derecha del mensaje
    factores = f.factorizar(n)
    if len(factores) == 2 and all(exp == 1 for exp in factores.values()): # si solo tiene dos factores y son primos distintos
        p1, p2 = factores.keys()
        # calculo por separado en modulos pequeños en vez de hacerlo con n que es muy grande y mas costoso
        cifrado_p1 = f.potencia_mod_p(m_pad % p1, e, p1)
        cifrado_p2 = f.potencia_mod_p(m_pad % p2, e, p2)
        inversa = f.inversa_mod_p(p2 % p1, p1)
        k = ((cifrado_p1 - cifrado_p2) * inversa) % p1
        cifrado = cifrado_p2 + p2 * k
        return cifrado
    else: # si la factorizacion no es de la forma que buscamos, lo hacemos mod n
        return f.potencia_mod_p(m_pad, e, n)


def descifrar_rsa(c:int,n:int,d:int,digitos_padding:int)->int:
    """Dado un cifrado c entero que haya sido cifrado con RSA usando
    digitos_padding cifras de padding al final del mensaje y el 
    módulo y exponente privado, n y d que formen la clave privada de RSA cuya pareja se
    utilizó para cifrar c, descifra c y elimina el padding, devolviendo
    el mensaje original.

    Args:
        c (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA usado para cifrar
        d (int): Exponente de la clave privada de RSA cuya pareja se utilizó para cifrar c
        digitos_padding (int): Número no negativo de cifras de padding usados para cifrar c
    
    Returns:
        int: entero resultante de descifrar c usando RSA con módulo m y exponente e y después eliminar el padding al resultado.

    Raises: None
    """
    factores = f.factorizar(n) # factorizamos para probar con el TCR
    if len(factores) == 2 and all(exp == 1 for exp in factores.values()):
        p1, p2 = factores.keys()
        # reducimos los exponentes -> reduce el coste de las potencias
        d_p1 = d % (p1 - 1)
        d_p2 = d % (p2 - 1)
        # desciframos por separado
        m_p1 = f.potencia_mod_p(c % p1, d_p1, p1)
        m_p2 = f.potencia_mod_p(c % p2, d_p2, p2)
        inversa = f.inversa_mod_p(p2 % p1, p1)
        h = ((m_p1 - m_p2) * inversa) % p1
        m_pad = m_p2 + p2 * h
    else: # si la factorizacion no es de la forma que buscamos, lo hacemos directamente mod n
        m_pad = f.potencia_mod_p(c, d, n)

    return eliminar_padding(m_pad, digitos_padding)


def codificar_cadena(s:str)->List[int]:
    """Convierte una cadena de caracteres a la lista de
    enteros que representa el valor unicode cada uno de sus caracteres.

    Args:
        s (str): cadena en texto plano

    Returns:
        int: lista de enteros que representan el código unicode de cada carácter de la cadena s.

    Raises: None.

    Example:
        codificar_cadena("¡Hola mundo!")=[161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33]
    """
    return list(ord(i) for i in s)


def decodificar_cadena(m:List[int])->str:
    """Convierte una lista de enteros que representen caracteres unicode
    en la cadena que representan.
    
    Args:
        m (List[int]): lisa de enteros que representan los códigos unicode de una cadena de caracteres.
    
    Returns:
        str: cadena que representan

    Raises:
        ValueError: Si alguno de los enteros no representa un caracter unicode válido.
    
    Example:
        decodificar_cadena([161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33])="¡Hola mundo!"
    """
    for codigo in m:
        if not (0 <= codigo <= 0x10FFFF): # 0x10FFFF es el maximo punto de codigo unicode permitido por estandar
            raise ValueError(f'El codigo {codigo} esta fuera del rango Unicode')
    
    return "".join(map(chr,m)) # aqui map(chr,m) es equivalente a decir -> chr(i) for i in m


def cifrar_cadena_rsa(s:str,n:int,e:int,digitos_padding:int)->List[int]:
    """
    Cifra carácter a carácter una cadena de caracteres usando RSA con clave púbica (n,e)
    y digitos_padding cifras de padding al final del mensaje y devuelve la lista de enteros
    que representan el mensaje cifrado correspondiente.
    Args:
        s (str): texto claro
        n (int): módulo para RSA
        e (int): clave pública para RSA
        digitos_padding (int): número no negativo de dígitos de padding que deben usarse para el cifrado del mensaje.
    
    Returns:
        List[int]: lista de enteros que representa el mensaje cifrado con RSA para la clave dada.

    Raises: None
    """
    cadena_cifrada = ""
    for char in s:
        char_ascii = ord(char)
        char_cifrado = cifrar_rsa(char_ascii, n, e, digitos_padding)
        cadena_cifrada.append(char_cifrado)
    return cadena_cifrada


def descifrar_cadena_rsa(cList:List[int],n:int,d:int,digitos_padding:int)->str:
    """Dado un mensaje cifrado con RSA usando la clave pública cuya clave privada asociada es (n,d)
    y digitos_padding cifras de padding al final del mensaje, devuelve la cadena orignal.
    Args:
        cList (List[int]): lisa de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        d (int): clave privada para RSA
        digitos_padding (int): número no negativo de dígitos de padding usados para el cifrado de cList.
    
    Returns:
        str: cadena que representa el texto claro correspondiente al mensaje cifrado cList.

    Raises:
        ValueError: Si, tras decodificar, alguno de los enteros del mensaje no representa un caracter unicode válido.    
    """
    #ERROR DE UNICODE
    cadena_descifrada = ""
    for c in cList:
        char_ascii = descifrar_rsa(c, n, d, digitos_padding)
        char = chr(char_ascii)
        cadena_descifrada += char
    return cadena_descifrada



def romper_clave(n:int,e:int)->int:
    """A partir de una clave pública válida (n,e), recupera la clave privada d tal que
    de = 1 (mod phi(n)).
    
    Args:
        n (int): módulo para RSA
        e (int): clave pública para RSA
    
    Returns:
        int: clave privada d

    Raises:
        ValueError: Si no existe ninguna clave privada d compatible con la clave pública (n,e).
    """
    phi = f.euler(n)
    if f.mcd(e, phi) != 1:
        raise ValueError('e y phi(n) no son coprimos por lo que no existe inversa')
    return f.inversa_mod_p(e, phi)


def ataque_texto_elegido(cList:List[int],n:int,e:int)->str:
    """Ejecuta un ataque de texto claro elegido sobre un mensaje que ha sido cifrado
    con RSA plano sin usar padding a partir de su clave pública.

    Args:
        cList (List[int]): lisa de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        e (int): clave pública para RSA
    
    Returns:
        str: texto plano descifrado para el mensaje cifrado cList

    Raises:
        ValueError: Si el mensaje no se corresponde con ningún texto plano que haya sido codificado con RSA sin padding.
    """
    # ERROR DE PADDING
    phi = f.euler(n)
    d = f.inversa_mod_p(e, phi)

    texto_descifrado = ""
    dic = {}
    for num in cList: 
        if num in dic:
            texto_descifrado += dic[num]
        else:
            char_ascii = f.potencia_mod_p(num, d, n)
            char = chr(char_ascii)
            texto_descifrado += char
            dic[num] = char

    return texto_descifrado
