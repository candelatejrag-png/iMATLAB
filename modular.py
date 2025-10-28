# importamos los scripts necesarios: 
import errores as e
import math

# Creamos error necesario: 
class IncompatibleEquationError(Exception): 
    pass

#  COMENZAMOS LA PRÁCTICA:

# Apartado 1

def es_primo(n:int) -> bool:
    """
    Toma un número (n) y valora si dicho número es primo positivo o no. 
    Se han realizado dos optimizaciones principales en el código:
        - No revisa todos los números hasta 'n', sino solo hasta '√n'.
        - Omite todos los números pares excepto el 2 (solo revisa impares)
    De esta manera se ha logrado llegar a una complejidad de O(√n/2) puesto a que solo recorre los numeros impares en el rango de 
    [3,√n]. 

    Args: 
        n (int): número que la función debe evaluar
    Returns: 
        (bool): devuelve True si n es primo y False de lo contrario
        """
    

    if n < 2:                                       # El 2 es el primo positivo más pequeño
        return False
    if n == 2:
        return True                                 # 2 es el único número primo par
    if n % 2 == 0:
        return False                                # Si es par y mayor que 2, no es primo
    for i in range(3, int(n**0.5) + 1, 2):      # Solo revisa impares hasta √n
        if n % i == 0:
            return False
    return True

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 2

def lista_primos(a:int, b:int) -> list[int]:
    """
    Devuelve los primos en el intervalo [a,b). 

    Args: 
        a (int): número donde empieza el intervalo
        b (int): número donde acaba el intervalo
    Returns: 
        res (list[int]): lista de primos del intervalo
    """

    result = []
    if a >= b:
        return result                   # Si a >= b, devuelve [] vacio
    largo = largo_lista(a,b)
    for x in range(max(2, a), b):       # Con max(2, a) evaluamos unicamente a partir del primer número primo positivo
        if posible_primos(x):
            result.append(x)            # Si el número es primo lo añadimos a la lista solución
        if len(result) == largo: 
            return result
    return result

def largo_lista(a: int, b: int) -> int: 
    if b <=1: 
        return 0
    return int((b/math.log10(b))-(a/math.log10(a))) if a > 1 else int((b/math.log10(b)))
    

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 3

def factorizar(n:int) -> dict[int, int]:
    """
    Toma un número y busca los primos positivos que lo dividan. Se realizan casos especiales para agilizar el proceso: el 2 y 3 son 
    múltiplos de la mayoría de números. Luego queda solo provar divisores de la forma 6k +/- 1. 
    Cada vez que se encuentra un factor:
        factors[p] = factors.get(p, 0) lee el contador del primo y si aun no estaba en el diccionario devuelve 0
        -> luego se le suma 1 (se ha encontrado que el divisor p esta presente más de una vez la descomposición factorial de n por tanto
        se suma 1 a su valor en el diccionario) y se vuelve a guardar. 
        ** si no pusieras el 0 a .get y la clave p aun no existiera en el dic, el valor por defecto seria None y None + 1 = Error
    Tras extraer 2 y 3, todo primo >= 5 es de la forma 6k-1 o 6k+1:
        posibles divisores restantes: 5, 7, 11, 13, 17, 19, 23, 25 ... (todos los coprimos de 2 y 3)
        los saltos son: +2, +4, +2, +4 ... (alternamos 2 y 4).

    Args: 
        n (int): número a evaluar
    Returns: 
        factors (dict[int,int]): diccionario cuyas claves nos los primos positivos que dividen a n y sus valores los exponentes a los
        que estan elevadas las claves en la descomposición factorial de n. 
    """

    if n in (-1, 0, 1): 
        return {}
    x = abs(n)
    factors = {}

    # potencias de 2
    while x % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        x //= 2

    # potencias de 3
    while x % 3 == 0:
        factors[3] = factors.get(3, 0) + 1
        x //= 3
    
    p_divisor = 5             # Primer 6k-1 (con k = 1)
    salto = 2                 # Primer salto sera +2
    while p_divisor * p_divisor <= x:
        while x % p_divisor == 0:
            factors[p_divisor] = factors.get(p_divisor, 0) + 1
            x //= p_divisor
        p_divisor += salto
        salto = 6 - salto     # Alterna 2,4 

    if x > 1:
        factors[x] = factors.get(x, 0) + 1
    
    return factors

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 4

def mcd(a:int, b:int) -> int:
    """
    Maximo comun divisor (algoritmo de Euclides)

    Args:
        a (int): primer componente del mcd
        b (int): segundo componente del mcd
    Returns:
        (int): devuelve el resultado del cálculo
    """
    a,b = max(a,b),min(a,b)
    while b:
        a, b = b, a % b

    return abs(a)

def bezout(a:int, b:int) -> tuple[int, int, int]:
    """
    Extensión del algoritmo de Euclides. Devuelve (g, x, y) tal que ax + by = d = mcd(a,b). El programa empezará por tomar el valor
    absoluto de los números y con un bucle realizará las operaciones del algoritmo, parará cuando el resto de una de dichas 
    operaciones sea 0. 

    Args: 
        a (int): primer componente del mcd
        b (int): segundo componente del mcd
    Returns: 
        (r_antes, x, y) (tuple[int,int,int]): 
        r_antes: es el mcd de a, b
        x, y: punto del plano que satisface la ecuación a*x_o + b*y_o = r_antes
    """

    r_antes, r = abs(a), abs(b)    
                                                # la izquierda
    x_antes, x = 1, 0                           # |a| = 1*|a| + 0*|b|
    y_antes, y = 0, 1                           # |b| = 0*|a| + 1*|b|
    while r >= 1:
        q = r_antes // r                        # Coeficiente de la división entera
        r_antes, r = r, r_antes - q*r           # Resto
        x_antes, x = x, x_antes - q*x           # Actualiza coeficiente de |a|
        y_antes, y = y, y_antes - q*y

    # max_cd, x_o, y_o = r_antes, x_antes, y_antes
    # if max_cd < 0:
    #     max_cd, x_o, y_o = -r_antes, -x_antes, -y_antes

    # En este punto, r_antes = mcd(|a|, |b|) y s_antes, t_antes son sus coeficientes
    x_o = x_antes if a >= 0 else -x_antes       # Corrige si a < 0
    y_o = y_antes if b >= 0 else -y_antes 
    
    return r_antes, x_o, y_o

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 5

def mcd_n(nlist:list[int]) -> int:
    """
    Máximo común divisor de una lista de enteros. Se calcula calculando el mcd de todos los enteros iterativamente hasta llegar al 
    resultado. Reducimos la complejidad empleando el teorema de euclides para resolverlo y si en algún momento el mcd = 1 hemos terminado. 
    
    Args: 
        nlist (list): lista con los números de los que se quiere saber el mcd
    Returns: 
        d (int): el valor de mcd(n1, n2, ..., nm)
    """
    d = 0
    for a in nlist:
        d = mcd(d, a)
        if d == 1:            # atajo: no puede bajar de 1
            return 1
    return d

def bezout_n(nlist:list[int]) -> tuple[int, list[int]]:
    """
    Aplica el teorema de bezout a n entradas iterativamente para encontrar el máximo común divisor entre todos ellos. 

    Args: 
        nlist (list): lista con todos los números de los que queremos hallar el máximo común divisor 
    Returns: 
        d, coefs (tuple): tupla compuesta por: 
            d (int): el resultado del mcd de todos los números
            coefs (list): los coeficientes asociados a cada número n de la lista de entrada de la fórmula de Bezout. 
    - Lista vacía -> ValueError.
    - Todos ceros -> (0, [0,...,0]).
    """
    n = len(nlist)
    if all(a == 0 for a in nlist):
        return 0, [0]*n

    # Inicializa con el primer término: d = |a1| = a1*(±1)
    d = abs(nlist[0])
    coefs = [0]*n
    coefs[0] = 1 if nlist[0] >= 0 else -1

    for i in range(1, n):     # Incorpora uno a uno usando Bézout: s*d + t*a = g
        a = nlist[i]
        g, s, t = bezout(d, a)
        
        for j in range(i):    # Escala los coeficientes existentes por s
            coefs[j] *= s
        coefs[i] = t          # Nuevo coeficiente para a_i
        d = g
        if d == 1:            # atajo si ya son coprimos
            return 1, coefs

    return d, coefs


'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 6

def coprimos(a:int, b:int) -> bool:
    """
    Calcula si dos números son coprimos empleando su defición. Dos números a y b son coprimos si (a, b) = 1.

    Args: 
        a (int): primer componente del mcd
        b (int): segundo componente del mcd
    Returns:
        (bool): True si son coprimos (se cumple la definición), False de lo contrario.
    """

    return mcd(a, b) == 1

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 7

def potencia_mod_p(base:int, exp:int, p:int) -> int:
    """
    Función que devuelve el número (result) congruente a otro (base) elevado a un cierto exponente (exp) con módulo (p). 
    Después de evaluar los casos base se empleará el método de exponenciación modular y exponenciación binaria para hallar el resultado de manera óptima. 

    Args: 
        base (int): la base del número
        exp (int): el exponente del número, antes de nada se validará que este sea positivo
        p (int): el módulo del número
    Returns:
        result (int): el resultado de la operación
    """
    if p == 0 or base == 0 and exp == 0: 
        raise ZeroDivisionError('No se puede dividir por 0 ni elevar a 0. ')
    if base < 0:                     # Actualizamos la base en el caso de que esta sea negativa
        base = p + base
    if exp < 0:                      # El exponente debe ser negativo, empleamos la fórmula b^e = b^(-1)*b^e
        base = inversa_mod_p(base,p)
        exp = abs(exp)

    if p == 1:
        return 0                     # Toda potencia es congruente a 0 (mod 1)
    
    base %= p                        # Normaliza base al rango [0, p - 1] 
    
    result = 1                       # Esto es simplemente un acumulador de factores
    while exp > 0:
        if exp % 2 == 1:             # Si exp impar -> 'usamos' la base, actualizamos el resultado
            result = (result * base) % p
        base = (base * base) % p     # Pasamos de b a b^2
        exp //= 2                    # Deslazamos el exponente -> quitamos el bit ya procesado
    return result

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 8

def inversa_mod_p(n:int, p:int) -> int:
    """
    Inversa de n modulo p, si existe. Lanza ValueError si no existe (d != 1). La calculamos empleando el teorema de bezout. 

    Args:
        n (int): entero cuyo inverso modular se busca
        p (int): módulo (positivo)
    Returns:
        (int): inverso de n modulo p en el rango [0, p-1] !!!!!!!!!!!!! por queeee ese rango
    """
    if p == 0: 
        raise ZeroDivisionError('No se puede dividir por 0. ')
    if p <= 1:
        raise e.NEError("NE")
    mcd_n_p, x_o, y_0 = bezout(n, p)    # Hacemos bezout 
    if mcd_n_p != 1:                    # Por definición
        raise ValueError('NE')
    # x puede ser negativo por lo que normalizamos al representante en [0, p-1] 
    # comoooo por queee
    return mod(x_o, p)

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 9

def euler(n:int) -> int:
    """
    Euler(n) devuelve el numero de enteros 1 <= k <= n que son coprimos con n. Se calculará empleando las propiedades que cumple esta
    función en relación con los números primos. 

    Args: 
        n (int): el número del que se quieren saber sus número de coprimos
    Returns: 
        phi (int): el valor de la función de Euler
    """
    if n == 0:
        return 0              # Por convenio
    if n < 0:                 # Para admitir negativos porque phi depende de los factores primos, no del signo
        raise ValueError('la función de Euler solo acepta enteros positivos. ')
    if n == 1:
        return 1
    f = factorizar(n)         # El diccionario {primo: exponente}
    phi = 1
    for p, e in f.items():    # Aplica la formula por factores primos
        phi *= (p ** (e - 1)) * (p - 1)
    return phi

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 10

def legendre(n:int, p:int) -> int:
    """Devuelve el simbolo de Legendre (n|p) para un primo impar p basando los cálculos en el criterio de Euler. 
    
    Args: 
        n (int): número al que se le quiere aplicar la función
        p (int): módulo de n
    Returns: 
        1:  n si es residuo cuadratico modulo p (existe x xon x^2 congruente de n (mod p))
        -1:  n no es residuo cuadratico modulo p
        0:  p|n (n congruente de 0 para (mod p)), p divide a n
    """
    if p == 0: 
        raise ZeroDivisionError('No se puede dividir por 0. ')
    if p <= 2 or not es_primo(p):
        raise ValueError("p debe ser primo impar")
    n_mod = n % p                                   # n|p
    if n_mod == 0:
        return 0
    val = potencia_mod_p(n_mod, (p - 1) // 2, p)    # el resto
    return -1 if val == p - 1 else int(val)         # int(val) solo puede ser 1

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 11 & 12

def mod(a:int, m:int) -> int:
    """
    Función que calcula el módulo entre dos números.

    Args: 
        a (int): primer número
        m (int): segundo número
    Returns: 
        (int): si m es > 0 devuelve el resto de la division entera
    """
    if m <= 0:
        raise ValueError("m debe ser > 0")
    return a % m

def tcr_dos(r1:int, m1:int, r2:int, m2:int) -> tuple[int, int]:
    """
    Resuelve un sistema de dos congruencias usando el Teorema Chino del Resto. Combina x = r1 (mod m1) y x = r2 (mod m2) para modulos
    no necesariamente coprimos. Lanza Value Error si no hay solucion. 

    Args: 
        r1 (int): número con módulo m1 congruente a x
        r2 (int): número con módulo m2 congruente a x
        m1, m2 (int): módulos de las dos ecuaciones a resolver
    Returns:
        res, lcm (tupla): devuelve la solución del sistema de dos congruencias en formato res (mod lcm) 
    """
    if m1 == 0 or m2 == 0:
        raise ValueError("modulo cero")                    # no dividir por 0
    if m1 < 0 or m2 < 0:
        raise ValueError("modulo negativo")
    d, s, _ = bezout(m1, m2)                               # d = mcd(m1, m2) y coeficientes de bezout
    if (r2 - r1) % d != 0:
        raise IncompatibleEquationError("incompatible")    # el sistema solo tiene solucion si d divide r2 - r1
    lcm = m1 // d * m2  
    k = ((r2 - r1) // d) * s
    res = (r1 + m1 * k) % lcm
    return res, lcm

def resolver_lineal(a:int, b:int, m:int) -> tuple[int, int]:
    """
    Resuleve el sistema de estructura a*x = b (mod m) Empleando el teotema de bezout. Lanza ValueError si no hay solucion

    Args: 
        a (int): número que multiplica a la x en la ecuación
        b (int): número con módulo p congruente a xa
        m (int): módulo de la ecuación
    Returns: 
        r, m1 (tuple): tupla solución en el formato r (mod m1) de tal modo que x = r (mod m1)
    """
    if m == 0:
        raise IncompatibleEquationError("modulo cero")
    if m < 0:
        raise ValueError("modulo negativo")
    d, x, _ = bezout(a, m)
    if b % d != 0:
        raise IncompatibleEquationError("sin solucion")
    a1, b1, m1 = a // d, b // d, m // d
    r = mod(x * b1, m1)
    return r, m1

def resolver_sistema_congruencias(alist, blist, plist):
    """
    Resuelve el sistema aix congruente a bi (mod pi). Acepta modulos no coprimos, lanza ValueError si no hay solucion
    Devuelve (r, m) con x congruente de r (mod m)

    Args: 
        alist (list): lista de todos los valores que multiplican a la x en cada ecuación
        blist (list): lista de todos los valores que con módulo p congruentes a aix
        plist (list): lista de todos los módulos de cada ecuación del sistema
    Returns: 
        r, m (tuple): devuelve la solución del sistema en formato de tupla de tal manera que la solución es r (mod m). 
    """
    n = len(alist)
    # primera ecuacion
    r, m = resolver_lineal(alist[0], blist[0], plist[0])          # comenzamos resolviendo la primera ecuación
    for i in range(1, n):
        r2, m2 = resolver_lineal(alist[i], blist[i], plist[i])    # resolvemos ecuación
        r, m = tcr_dos(r, m, r2, m2)                              # empleando el teorema chino del resto dos a dos valos resolviendo todo el sistema


    return mod(r, m), m                                           # se devuelve r reducido al rango [0, m - 1] y el modulo m

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 15: 

def carmichael(n:int) -> int:
    """
    Devuelve lambda(n), exponente (el menor x >= 1) tal que a^x congruente 1(mod n) para todo a coprimo con n
    Requiere n > 0
    Para n = 1, por convenio lambda(1) = 1
    Factoriza n en {p: e} y calcula lambda(p^e) según las fórmulas detalladas en nuestra memoria
    Acumula el resultado haciendo mcm, que lo calculamos con mcd
    """
    if n <= 0:
        raise ValueError("n debe ser > 0")
    if n == 1:
        return 1
    
    fac = factorizar(n) # se queda como {p: e}
    lam = 1
    for p, e in fac.items():
        if p == 2:
            if e == 1:
                lam_pe = 1
            elif e == 2:
                lam_pe = 2
            else:
                lam_pe = 2 ** (e -2) 
        else:
            lam_pe = (p - 1) * (p ** (e - 1))
        
        lam = lam // mcd(lam, lam_pe) * lam_pe
    return lam

'-------------------------------------------------------------------------------------------------------------------------------------'
# Mejoras para la practica 2:
# Con el fin de optimizar los algorítmos empleados en la práctica 2 se han implementado dos funciones: posible_primos y fcatorizar_cripto. 


def posible_primos(n: int) -> bool: 
    '''Función que evalúa si un número n es primo empleando el test de primaridad de Miller-Rabin. Este se basa en el pequeño teorema de Fermat
    y en la propiedad que dice que si un número n es primo las únicas raíces cuadradas de 1 (mod n) son 1 (mod n) o -1 (mod n). 
    
    Args: 
        n (int): número del que se va a evaluar su primaridad. 
    Returns: 
        _ (bool): se devuelve True si el número es primo y False de lo comtrario. 
    '''
    if n < 2:                 # El 2 es el primo positivo más pequeño
        return False
    if n in (2, 3):
        return True           # 2 es el único número primo par
    if n % 2 == 0:
        return False          # Si es par y mayor que 2, no es primo
    # Buscamos escribir n como 2^s*d + 1
    d = n - 1
    s = 0
    while d % 2 == 0:           # eliminamos todos los factores de 2 posibles de d y actualizamos la s. 
        d //= 2
        s += 1
    x = potencia_mod_p(2, d, n) 
    if x == 1 or x == n - 1:    # Comprobamos si se cumple el Teorema, si es así el número es primo
        return True
    for _ in range(s - 1):      # Si no se cumple debemos comprobar toda la secuencia de números calculada
        x = potencia_mod_p(x, 2, n)
        if x == n - 1:          # Si para algún número de la secuencia la congruencia es -1 se cumple la propiedad, n es primo
            return True
    return False              # Si no se cumple la propiedad para ningún número de la secuencia n no es primo

def factorizar_cripto(n: int) -> tuple[int, int]:
    # mas optimo si los factores son cercanos entre si y cerca de sqrt(n)
    '''Función que factoriza un número sabiendo que este es producto de dos primos enpleando el método de Factorización de Fermat. Primero, 
    en el caso de que n sea par y, sabiendo que es producto de dos primos tendremos n = 2*d con d = n//2.Por otro lado, si n es impar buscaremos
    su producto de primos representandolo como la diferencia de dos cuadrados. 
    
    Args: 
        n (int): el número a factorizar. 
    Returns: 
        lista (list): lista con los primos que forman n. (Ya que sabemos la estructura de n no es necesario almacenar la información en un 
        diccionario como se hace en la función de factorizar() ya que aquí sabemos que los primos que componen al número tienen exponente 1.)
    '''
    if n % 2 == 0:         # si n es par ya sabemos cuál será su factroización
        return 2, n // 2
                           # Si n es impar empleamos el método de factorización de Fermat para encontrar el producto de primos
    x = math.isqrt(n)      # Obtenemos un primer valor de x
    if x * x < n:
        x += 1

    while True:
        y2 = x * x - n     # Obtenemos un primer valor de y
        y = math.isqrt(y2)
        if y * y == y2:    # Si se cumple la ecuación x^2 -y^2 = n hemos terminado
            return x - y, x + y
        x += 1

def factorizar_cripto_2(n:int) -> tuple[int, int]: 
    # mas optimo si los factores no son cercanos entre si
    """
    Factorizamos n suponiendo que es semiprimo: n = p1 * p2 con p1, p2 primos
    Empieza a buscar divisores en suelo(sqrt(n)) y desciende (solo checkeando impares)
    Devuelve (p1, p2) con p1 <= p2 en cuanto encuentra un divisor

    Si n es par, devuelve (2, n // 2)
    Si n es un cuadrado perfecto, devuelve (sqrt(n), sqrt(n))
    Lanza ValueError si no encuentra divisor > 1: n es primo o no semiprimo
    """

    if n % 2 == 0: # 2 * p2 (p2 primo impar)
        return 2, n // 2
    
    # chequeamos si es cuadrado perfecto
    r = int(n ** 0.5)
    if r * r == n:
        return (r, r)

    # empezamos desde suelo(sqrt(n)) y bajamos por impares buscando los primos
    if r % 2 == 1:
        factor = r
    else:
        factor = r - 1
    
    while factor >= 3:
        if n % factor == 0: # f y n|f factores
            p1, p2 = factor, n // factor
            if p1 > p2:
                p1, p2 = p2, p1
            return (p1, p2)
        factor -= 2 # solo impares


        
