# importamos los scripts necesarios: 
import errores as e

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
    for i in range(3, int(pow(n,0.5)) + 1, 2):      # Solo revisa impares hasta √n
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
    for x in range(max(2, a), b):       # Con max(2, a) evaluamos unicamente a partir del primer número primo positivo
        if es_primo(x):
            result.append(x)            # Si el número es primo lo añadimos a la lista solución
    return result
    

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
    Extensión del algoritmo de Euclides. Devuelve (g, x, y) tal que ax + by = g = mcd(a,b). El programa empezará por tomar el valor
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

    r_antes, r = a, b   
                                                # la izquierda
    s_antes, s = 1, 0                           # |a| = 1*|a| + 0*|b|
    t_antes, t = 0, 1                           # |b| = 0*|a| + 1*|b|
    while r >= 1:
        q = r_antes // r                        # Coeficiente de la división entera
        r_antes, r = r, r_antes - q*r           # Resto
        s_antes, s = s, s_antes - q*s           # Actualiza coeficiente de |a|
        t_antes, t = t, t_antes - q*t

    # En este punto, r_antes = mcd(|a|, |b|) y s_antes, t_antes son sus coeficientes
    x_o = s_antes if a >= 0 else -s_antes       # Corrige si a < 0
    y_o = t_antes if b >= 0 else -t_antes 
    
    return r_antes, x_o, y_o

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 5

def mcd_n(nlist:list[int]) -> int:
    """
    Máximo común divisor de una lista de enteros.
    - Lista vacía -> ValueError.
    - Todos ceros -> 0.
    1. reduce con Euclides
    2. Si en algun punto g = 1, termina (atajo)
    """
    if not nlist:
        raise ValueError("lista vacía")
    g = 0
    for a in nlist:
        g = mcd(g, a)
        if g == 1:            # atajo: no puede bajar de 1
            return 1
    return g

def bezout_n(nlist:list[int]) -> tuple[int, list[int]]:
    """
    Devuelve coeficientes de Bézout para n enteros.
    Devuelve (d, coefs) con d = mcd(nlist) y sum(a_i*coefs[i]) = d.
    - Lista vacía -> ValueError.
    - Todos ceros -> (0, [0,...,0]).
    """
    if not nlist:
        raise ValueError("lista vacía")
    n = len(nlist)
    if all(a == 0 for a in nlist):
        return 0, [0]*n

    # Inicializa con el primer término: d = |a1| = a1*(±1)
    d = abs(nlist[0])
    coefs = [0]*n
    coefs[0] = 1 if nlist[0] >= 0 else -1

    # Incorpora uno a uno usando Bézout: s*d + t*a = g
    for i in range(1, n):
        a = nlist[i]
        g, s, t = bezout(d, a)
        # Escala los coeficientes existentes por s
        for j in range(i):
            coefs[j] *= s
        # Nuevo coeficiente para a_i
        coefs[i] = t
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
    Primero afrontaremos el posible caso de módulo = 1, esto devuelve un 0 automáticamente, despúes normalizaremos la base por
    eficiencia

    Args: 
        base (int): la base del número
        exp (int): el exponente del número, antes de nada se validará que este sea positivo
        p (int): el módulo del número
    Returns:
        result (int): el resultado de la operación
    """
    if p == 0 or base == 0 or exp == 0: 
        raise ZeroDivisionError('No se puede dividir por 0. ')
    if base < 0: 
        base = p + base
    if exp < 0: 
        base = inversa_mod_p(base,p)
        exp = abs(exp)

    if p == 1:
        return 0                                   # Toda potencia es congruente a 0 (mod 1)
    
    base %= p                                      # Normaliza base al rango [0, p - 1] 
    

    """
    Exponenciacion modular -> usado en criptografia -> source: WIKIPEDIA
    Muy eficiente, podemos pasar de O(e) a O(log(e)) 
    https://es.wikipedia.org/wiki/Exponenciaci%C3%B3n_modular
    Que es lo que entiendo por ahora de exponenciacion modular:
        - si queremos calcular a^e mod p sin construir a^e que puede ser muy grande
        - usamos el truco de 'cuadrar y multiplicar':
            - si e es par: b^e = (b^2)^(e/2)
            - si e es imapar: b^e = b*(b^2)^((e-1)/2)
    Preguntar:
        - por que es invariante, algo que ver con el pequeño teorema?
        - no veo como cuadra la base
    """
    result = 1  # esto es simplemente un acumulador de factores
    while exp > 0:
        if exp % 2 == 1:     # si exp impar -> 'usamos' la base
            result = (result * base) % p
        base = (base * base) % p     # pasamos de b a b^2
        exp //= 2          # deslazamos el exponente -> quitamos el bit ya procesado
    return result

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 8

def inversa_mod_p(n:int, p:int) -> int:
    """
    Inversa de n modulo p, si existe. Lanza ValueError si no existe (g != 1)

    Args:
        n (int): entero cuyo inverso modular se busca
        p (int): módulo (positivo)
    Returns:
        (int): inverso de n modulo p en el rango [0, p-1] !!!!!!!!!!!!! por queeee ese rango
    """
    if p == 0: 
        raise ZeroDivisionError('No se puede dividir por 0. ')
    if p <= 1:
        raise e.NEError("NE") # siii!!! por queee
    mcd_n_p, x_o, y_0 = bezout(n, p)    # Hacemos bezout 
    if mcd_n_p != 1:                    # Por definición
        raise ZeroDivisionError(f"No existe inversa: mcd({n}, {p}) = {mcd_n_p} != 1")
    # x puede ser negativo por lo que normalizamos al representante en [0, p-1] 
    # comoooo por queee
    return mod(x_o, p)

'-------------------------------------------------------------------------------------------------------------------------------------'

# Apartado 9

def euler(n:int) -> int:
    """
    euler(n) devuelve el numero de enteros 1 <= k <= n que son coprimos con n
    """
    if n == 0:
        return 0              # Por convenio
    n = abs(n)                # Para admitir negativos porque phi depende de los factores primos, no del signo
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
    """Devuelve el simbolo de Legendre (n|p) para un primo impar p
    Valores posibles:
        1 -> n si es residuo cuadratico modulo p (existe x xon x^2 congruente de n (mod p))
        -1 -> n no es residuo cuadratico modulo p
        0 -> p|n (n congruente de 0 para (mod p))
    ** pow(base, exp, m) es la potencia modular de python
        y devuelve: (base^exp) mod m
    --> la usamos porque es mucho mas eficiente que elevar y luego hacer %    
    """
    if p == 0: 
        raise ZeroDivisionError('No se puede dividir por 0. ')
    if p <= 2 or not es_primo(p):
        raise ValueError("p debe ser primo impar")
    n_mod = n % p                               # n|p
    if n_mod == 0:
        return 0
    val = pow(n_mod, (p - 1) // 2, p)           # el resto
    return -1 if val == p - 1 else int(val)     # int(val) solo puede ser 1

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
    # !!!!!!!!! CAMBIADO EL COMMENT MIRALO
    if m <= 0:
        raise ValueError("m debe ser > 0")
    return a % m



def tcr_dos(r1:int, m1:int, r2:int, m2:int) -> tuple[int, int]:
    """
    Resuelve un sistema de dos congruencias usando el Teorema Chino del Resto
    Combina x = r1 (mod m1) y x = r2 (mod m2) para modulos no necesariamente coprimos
    Lanza Value Error si no hay solucion

    """
    if m1 == 0 or m2 == 0:
        raise ValueError("modulo cero")     # no dividir por 0
    if m1 < 0 or m2 < 0:
        raise ValueError("modulo negativo")
    g, s, _ = bezout(m1, m2)                # g = mcd(m1, m2) y coeficientes de bezout
    if (r2 - r1) % g != 0:
        raise IncompatibleEquationError("incompatible")    # el sistema solo tiene solucion si g divide r2 - r1
    lcm = m1 // g * m2  
    k = ((r2 - r1) // g) * s
    res = (r1 + m1 * k) % lcm
    return res, lcm

def resolver_lineal(a:int, b:int, m:int) -> tuple[int, int]:
    """
    Resuleve a*x = b (mod m)
    Devuelve (r, mod') con x = r (mod mod')
    Lanza ValueError si no hay solucion
    """
    if m == 0:
        raise ValueError("modulo cero")
    if m < 0:
        raise ValueError("modulo negativo")
    g, s, _ = bezout(a, m)
    if b % g != 0:
        raise IncompatibleEquationError("sin solucion")
    a1, b1, m1 = a // g, b // g, m // g
    r = mod(s * b1, m1)
    return r, m1

def resolver_sistema_congruencias(alist, blist, plist):
    """
    Resuelve el sistema aix congruente a bi (mod pi)
    Acepta modulos no coprimos, lanza ValueError si no hay solucion
    Devuelve (r, m) con x congruente de r (mod m)
    """
    n = len(alist)
    # if n == 0 or n != len(blist) or n != len(plist):
    #     raise ValueError("entrada vacia o inconsistente")
    
    # primera ecuacion
    r, m = resolver_lineal(alist[0], blist[0], plist[0])
    for i in range(1, n):
        r2, m2 = resolver_lineal(alist[i], blist[i], plist[i])
        r, m = tcr_dos(r, m, r2, m2)


    return mod(r, m), m               # se devuelve r reducido al rango [0, m - 1] y el modulo m

'-------------------------------------------------------------------------------------------------------------------------------------'

# 14
def ec_cuadratica(a:int, b:int, c:int, p:int):
    """
    Devuelve las dos raices (posiblemente iguales) de ax^2 + bx + c = 0 (mod p) con p primo
        - si no hay raices: devuelve None
        - si hay dos raices: (x1, x2) con x1 < x2
        - si hay una doble: (x, x)
    Casos como a = 0 (mod p) se tratan como ecuacion lineal
    """
    if p <= 1 or not es_primo(p):
        raise ValueError("p debe ser primo")
    a %= p
    b %= p
    c %= p

    if a == 0:
        # bx + c = 0 (mod p)
        if b == 0:
            if c == 0:
                # infinitas soluciones -> por convencion devolvemos (0,0)
                return (0, 0)
            else:
                return None
        x = (-c * inversa_mod_p(b, p)) % p
        return (x, x)
    
    # discriminante
    delta = (b*b -4*a*c) % p
    r = raiz_mod_p


# 12. (Opcional) Expandir la funcionalidad de resolver sistema congruencias y del comando resolverSistema para
# resolver sistemas de ecuaciones donde los m´odulos no son coprimos entre s´ı.
# 13. (Opcional) Investigar el algoritmo de Cipolla y programar en “modular.py” una funci´on
# raiz mod p(n : int, p : int) −→ int
# que reciba un entero n y un n´umero primo p y calcule una ra´ız de n m´odulo p, es decir, un entero x tal que
# x
# 2 ≡ n (mod p)
# Usando dicha funci´on, agregar a IMAT-LAB un comando
# raiz(n, p)
# que devuelva lo siguiente:
#  Si n tiene dos ra´ıces distintas x1 < x2, las escribe en orden: “x1, x2”
#  Si n tiene una ´unica ra´ız x, escribe “x”
#  Si n no tiene ra´ıces, como con el resto de comandos, escribe “NE” en modo “batch” o un mensaje de error
# adecuado en modo interactivo.
# 14. (Opcional) Usando la funci´on anterior, implementar en “modular.py” una funci´on
# ecuacion cuadratica(a : int, b : int, c : int, p : int) −→ T uple[int, int]
# que reciba enteros a, b, c y p, con p n´umero primo, y devuelva las dos soluciones m´odulo p (posiblemente repetidas)
# de la ecuaci´on
# ax2 + bx + c ≡ 0 (mod p)
# Usando dicha funci´on, agregar a IMAT-LAB un comando
# ecCuadratica(a, b, c, p)
# que implemente la funcionalidad anterior y devuelva lo siguiente
#  Si la ecuaci´on tiene dos ra´ıces distintas x1 < x2, las escribe en orden: “x1, x2”
#  Si la ecuaci´on tiene una ´unica ra´ız doble x, escribe “x”
#  Si la ecuaci´on no tiene ra´ıces, como co








