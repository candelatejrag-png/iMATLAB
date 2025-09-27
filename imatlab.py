# Importamos las librerías necesarias:
import sys

# importamos los scripts necesarios: 
import modular2 as f
import errores as e
import re 

# Implementamos las funciones que van a ser empleadas en el programa: 
def run_commands(fin, fout): 
    pass

def clean_command(comando_sucio: str, dic_comandos: dict) -> tuple:
    '''Función que limpia y valida los comandos recibidos por pantalla encontrando la función de modular.py que se corresponde con la que pide el usuario expleando expresiones
    regurales en leguaje Regex con el fin de volver la búsqueda más eficiente. En el caso de que el usuario haya introducido el comando mal se lanzará un NOPError.  
    
    Args:
        comando_sucio (str): string escrito por el usuario. 
        dic_comandos (dict): diccionario que contiene como clave los nombres de cada función que debe introducir el usuario y como valores listas. En la primera posición de la 
        lista (posición 0 en indexación de python) encontramos el la función de modular.py asociada al comando que se ha pedido por pantalla y en la segunda posición
        el número de argumentos (números enteros) que se deben de haber introducido para resolver la operación. 
    Returns: 
        comando_limpio (tuple): se devuelve una tupla con la función que se va a ejecutar y la lista de argumentos (previamente convertidos a tipo int). 
       '''
    
    # Empleando expresiones regulares creamos el patrón de la estructura que debe tener el input de pantalla (comando(Argumentos)). Esta expresión se divide en dos grupos. El 
    # primero corresponde al comando que se quiere realizar (más adelante se validará si este es válido) y el segundo a todo lo que este dentro de los parentesís de forma 
    # perezosa (lazy). Más adelante se válidará si lo que se encuentra dentro del paréntesis tiene el formato adecuado. 
    
    pattern = re.compile(r"([a-zA-Z_]+)+\((.*?)\)")

    match = re.search(pattern, comando_sucio)
    if not match:                                                              # Si el comando introducido por el usuario no tiene un formato adecuado lanzamos una excepción.
        raise e.NOPError('El formato introducido no es el adecuado, introduzca comando(argumentos) para realizar la operación. Recuerde no introducir espacios entre los argumentos.')
    
    comando = match.group(1)
    if comando not in dic_comandos:                                            # Si el comando no esta en el diccionario no forma parte de nuestra librería, lanzamos una excepción. 
        raise e.NOPError(f'El comando {comando} no exsite. ')
    
    lista_argumentos = re.findall(r"-?\d+", match.group(2))                    # Empleamos el método findall junto a la expresión '-?\d+' que nos creará una lista solo con los números que encuentre en el grupo 2. 
    if len(lista_argumentos) != dic_comandos[comando][1]:                      # Si esta lista no tiene los números necesarios para la operación se lanza una excepción. 
        raise e.NOPError(f'El comando {comando} no se puede realizar con los argumentos dados. Se han introducido {len(lista_argumentos)} válidos cuándo se necesitaban {dic_comandos[comando][1]}. ')
    comando_limpio = (dic_comandos[comando][0], map(int, lista_argumentos))    # creamos el diccionario solución convirtiendo los argumentos en enteros empleando map(int, args)
    return comando_limpio 


if __name__ == '__main__': 

    # Creamos un diccionario donde la clave es la función que pide el usuario y su valor asociado es una lista formada por la función de modular.py asociada al comando y el número 
    # de argumentos que recibe la función. 
    dic_comandos = {'primo':[ f.es_primo, 1],'primos': [f.lista_primos, 2], 'factorizar': [f.factorizar, 1], 'mcd': [f.mcd, 2], 'coprimos': [f.coprimos, 2], 'pow': [f.potencia_mod_p, 3], 'inv': [f.inversa_mod_p, 2], 'euler': [f.euler, 1], 'legendre': [f.legendre, 2], 'resolversistema': [f.resolver_sistema_congruencias, 3]}

    if len(sys.argv) == 1:              # Si no se han recibido datos por la terminal pasamos al modo automático, trabajamos con ficheros
        run_commands()
    else: 
                                        # Procesamos los datos recibidos.   
        try:
            funcion, args = clean_command(sys.argv[1], dic_comandos)
            result = funcion(*args)     # Llamamos a la función, empleando '*' le pasamos cada elemento de la lista a cada argumento. 
            
        except e.NOPError as error: 
            print(error)
        
        