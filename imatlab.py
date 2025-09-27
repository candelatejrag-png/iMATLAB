# Importamos las librerías necesarias:
import sys

# importamos los scripts necesarios: 
import modular2 as f
import errores as e
import re 

# Implementamos las funciones que van a ser empleadas en el programa: 
def run_commands(fin, fout): 
    pass

def clean_command(comando_sucio: list[str], dic_comandos: dict) -> dict:
    '''Función que limpia los comandos recibidos por pantalla encontrando la función de modular.py que se corresponde con la que pide el usuario. 
    Del mismo modo, utilizando algunas funciones auxiliares, COMENTO LUEGO!!!!!!!!!!'''
    
    # Empleando expresiones regulares vemos si el usuario ha ejecutado el comando correctamente. ç
    pattern = re.compile(r"([a-zA-Z_]+)+\((.*?)\)")

    comando_limpio = {}
    match = re.search(pattern, comando_sucio)
    comando = match.group(1)
    if comando not in dic_comandos: 
        raise e.NOPError(f'El comando {comando} no exsite. ')
    comando_limpio[dic_comandos[comando]] = re.findall(r"-?\d+", match.group(2))
    return comando_limpio


if __name__ == '__main__': 

    # Creamos un diccionario donde la clave es la función que pide el usuario y su valor asociado es una lista formada por la función de modular.py asociada al comando y el número de argumentos que recibe la función. 
    dic_comandos = {'primo': 'es_primo','primos': 'lista_primos', 'factorizar': 'factorizar', 'mcd': 'mcd', 'coprimos': 'coprimos', 'pow': 'potencia_mod_p', 'inv': 'inversa_mod_p', 'euler': 'euler', 'legendre': 'legendre', 'resolversistema': 'resolver_sistema_congruencias'}

    # Procesamos los datos recibidos por los argumentos de la terminal, lidiamos con los posibles errores y con el caso de que no haya argumentos. 
    if len(sys.argv) == 1: 
        run_commands()
    else: 
        try:
            dic = clean_command(sys.argv[1:])
        except e.NOPError as error: 
            print(error)
        print(dic)









    
    # if len(sys.argv) == 2: 

    #     pass

    # else: 
    #     if len(sys.argv) != 1: 
    #         print('El formato no es adecuado, no se podrá realizar la operación. ')
    #     else: 
    #         print('No se ha introducido ningún comando, se ejecutarán unas operaciones de manera automática. ')
    #         run_commands()
