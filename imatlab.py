"""
imatlab.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP10
Integrantes:
    - Candela Tejedo Raga
    - Gabriela Romero Martín

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este script se ejecuta sin parámetros,
lanzaría la interfaz de usuario para el modo interactivo.
"""

# Importamos las librerías necesarias:
from typing import TextIO
import sys
import os

# importamos los scripts necesarios: 
import modular as f
import modular
import errores as e
import re 

# Implementamos las funciones que van a ser empleadas en el programa: 

def clean_command(comando_sucio: str, dic_comandos: dict) -> tuple:
    '''Función que limpia y valida los comandos recibidos por pantalla encontrando la función de modular.py que se corresponde con la que pide el usuario expleando expresiones
    regurales en leguaje Regex con el fin de volver la búsqueda más eficiente. En el caso de que el usuario haya introducido el comando mal se lanzará un NOPError.  
    Empleando expresiones regulares creamos el patrón de la estructura que debe tener el input de pantalla (comando(Argumentos)). Esta expresión se divide en dos grupos. El 
    primero corresponde al comando que se quiere realizar (más adelante se validará si este es válido, si tiene una fucnión de modular.py asociada) y el segundo a todo lo que
    este dentro de los parentesís de forma perezosa (lazy). Más adelante se válidará si lo que se encuentra dentro del paréntesis tiene el formato adecuado haciendo uso del método 
    findall que, junto a la expresión -?[0-9]+ que nos creará una lista solo con los números (todavia serán tipo int, eso se cambiará más adelante) que encuentre en el grupo 2 
    (el grupo de los argumentos).
    
    Ejemplo: 
        Al aplicarle esta función a pow(2,3,4) se devolverá: (f.potencia_mod_p, [2,3,4])
    Args:
        comando_sucio (str): string escrito por el usuario. 
        dic_comandos (dict): diccionario que contiene como clave los nombres de cada función que debe introducir el usuario y como valores listas. En la primera posición de la 
        lista (posición 0 en indexación de python) encontramos el la función de modular.py asociada al comando que se ha pedido por pantalla y en la segunda posición
        el número de argumentos (números enteros) que se deben de haber introducido para resolver la operación. 
    Returns: 
        comando_limpio (tuple): se devuelve una tupla con la función que se va a ejecutar y la lista de argumentos (previamente convertidos a tipo int). 
    '''
    
    pattern = re.compile(r"([a-zA-Z_]+)+\((.*?)\)")

    match = re.search(pattern, comando_sucio)
    if not match:                                                                                                  # Si el comando introducido por el usuario no tiene un formato adecuado lanzamos una excepción.
        raise e.NOPError('El formato introducido no es el adecuado, introduzca comando(argumentos) para realizar la operación. Recuerde no introducir espacios entre los argumentos.')
    
    comando = match.group(1)
    if comando not in dic_comandos:                                                                                # Si el comando no esta en el diccionario no forma parte de nuestra librería, lanzamos una excepción. 
        raise e.NOPError(f'NOP')
    comando_nuevo, llamar_comando = dic_comandos[comando][0], dic_comandos[comando][2]
    if comando_nuevo == f.resolver_sistema_congruencias:                                                           # Los argumentos de esta función tiene una estructura distinta
        longitud = len(match.group(2).split(','))
        match_r_sist = re.findall(r"\[(-?\d+);(-?\d+);(-?\d+)\]", match.group(2))
        lista_argumentos = list(map(list, zip(*(map(int,num) for num in match_r_sist))))
        if match_r_sist == [] or longitud != len(lista_argumentos[0]): 
            raise e.NOPError(f'El comando {comando} no se puede realizar con los argumentos dados. ')

    else:
        lista_argumentos = re.findall(r"-?\d+", match.group(2))             
        if lista_argumentos == [] or (dic_comandos[comando][1] is not None and len(lista_argumentos) != dic_comandos[comando][1]):             # Si esta lista no tiene los números necesarios para la operación se lanza una excepción. 
            raise e.NOPError(f'El comando {comando} no se puede realizar con los argumentos dados. Se han introducido {len(lista_argumentos)} válidos cuándo se necesitaban {dic_comandos[comando][1]}. ')
        lista_argumentos = map(int, lista_argumentos)
    comando_limpio = (comando_nuevo, llamar_comando, lista_argumentos)                                             # creamos la tupla solución convirtiendo los argumentos en enteros empleando map(int, args)
    return comando_limpio 

def run_bool(funcion, args: list): 
    result = funcion(*args)
    return 'Sí' if result else 'No'

def run_lprimos(funcion, args: list): 
    result = funcion(*args)
    return str(result)[1:-1] if len(result) != 0 else 'NE'

def run_factors(funcion, args: list): 
    result = funcion(*args)
    return str(result)[1:-1] if len(result) != 0 else 0

def run_mcd(funcion, args: list): 
    if args != 2: 
        return f.mcd_n(args)
    return funcion(*args)

def run_mod_p(funcion, args: list): 
    try: 
        return funcion(*args)
    except ZeroDivisionError as error: 
        return 'NE'
    except e.NOPError as error: 
        return 'NOP'
    except ValueError as error: 
        return error
    
def run_resSist(funcion, args: list): 
    try: 
        r, m = funcion(*args)
        return f'{r} (mod {m})'
    except ValueError as error: 
        return error
    except modular.IncompatibleEquationError as error: 
        return error

def run_program(comando_sucio, user=True):

    # Creamos un diccionario donde la clave es la función que pide el usuario y su valor asociado es una lista formada por la función de modular.py asociada al comando y el número 
    # de argumentos que recibe la función.  
    dic_comandos = {'primo':[ f.es_primo, 1, run_bool],'primos': [f.lista_primos, 2, run_lprimos], 'factorizar': [f.factorizar, 1, run_factors], 'mcd': [f.mcd, None, run_mcd], 'coprimos': [f.coprimos, 2, run_bool], 'pow': [f.potencia_mod_p, 3, run_mod_p], 'inv': [f.inversa_mod_p, 2, run_mod_p], 'euler': [f.euler, 1, run_mod_p], 'legendre': [f.legendre, 2, run_mod_p], 'resolverSistema': [f.resolver_sistema_congruencias, None, run_resSist], 'mcd_n':[f.mcd_n, None, run_mcd]}
    try: 
        funcion, llamar_fun, args = clean_command(comando_sucio, dic_comandos)
        result = llamar_fun(funcion, args)     # Llamamos a la función, empleando '*' le pasamos cada elemento de la lista a cada argumento. 
        return result
    except e.NEError as error: 
        return error
    except e.NOPError as error: 
        return error


def run_commands(fin: TextIO, fout: TextIO): 
    """ Recibe un manejador fin de un fichero de texto ya abierto para lectura y otro de un fichero de salida
    ya abierto para escritura y ejecuta línea por línea los comandos proporcionados por fin, escribiendo los resultados en fout.
    Si fin y fout no corresponden con la entrada y salida esáandar, esta función ejecuta el modo de procesamiento
    por lotes de IMAT-LAB para la entrada fin, guardando el resultado en el fichero fout.

    Args:
        fin (TextIO): Fichero de entrada. Manejador de un fichero de texto ya abierto para lectura.
        fout (TextIO): Fichero de salida. Manejador de un fichero de texto ya abierto para escritura.
    
    Returns: None
    
    Raises: None
    
    Examples:
        run_commands(sys.stdin,sys.stdout) lanza el modo interactivo y ejecuta línea por línea los comandos que
            el usuario lanza desde la entrada estándar.
    """
    for linea in fin: 
        result = run_program(linea.strip(), False)
        if result is not None:
            fout.write(str(result)+'\n')


if __name__ == '__main__': 

    if len(sys.argv) == 3:                        # Si se han recibido ficheros por la terminal se ejecuta el programa en modo lotes. 
        if os.path(sys.argv(2)):                  # Validamos si el fichero de entrada existe, de lo contrario salimos del programa. 
            with open(sys.argv(2), 'r') as fin: 
                with open(sys.argv(3), 'w', encoding='utf-8') as fout: 
                    run_commands(fin, fout)
        else: 
            print('El nombre del fichero introducido no existe. ')
    else:                                         # Si no se han recibido los argumentos correctos se ejecuta el modo interactivo. 
        if len(sys.argv) != 1:                    # Aviso que salta si ha recibido algún argumento de manera erronea. 
            print('El número de argumentos dados no es válido. ')
        nuevo_comando = input('Introduce una operación (Enter para salir): ')
        while nuevo_comando != '':
            print(run_program(nuevo_comando))     # Ejecutamos el programa.  
            nuevo_comando = input('Nueva operación (Enter para salir): ')
    print('Has salido del programa. ')