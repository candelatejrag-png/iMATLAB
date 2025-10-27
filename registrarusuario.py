# Importamos los ficheros necesarios.
import rsa as f

# Importamos las librerías necesarias. 
from pathlib import Path

# Creamos las funciones necesarias para la ejecución del programa. 

def almacenar(ruta_fichero: str, datos: list): 
    '''Función que crear el fichero dentro de la carpeta usuarios con el nombre recibido por argumentos y almacena en su interior datos recibidos también por argumentos. 
    
    Args: 
        nombre_fichero (str): el nombre del fichero donde se almacena la información. 
    Returns: 
        datos (list): lista que contiene todos los datos que se quieren almacenar dentro del fichero. 
        '''
    with open(ruta_fichero, 'w', encoding='utf-8') as fi: 
        for dato in datos: 
            fi.write(f'{dato}\n')

if __name__ == '__main__': 
 
    # Comenzamos solicitandole al usuario la información necesaria.
    nombre = input('Un nombre: ')
    val_min = input('Introduzca el valor mínimo de cada primo usado para generar sus claves RSA: ')
    val_max = input('Introduzca el valor máximo de cada primo usado para generar sus claves RSA: ')
    pad = input('Introduzca el número de padding para la comunicación con el usuario. ')
    
    # Generamos las claves públicas y privada del usuario a partir de la información recogida capturando los posibles errores. 
    try:
        pad = int(pad)                                # Comprobamos que el dato recibido por pantalla es válido
        n,e,d = map(str,f.generar_claves(int(val_min), int(val_max)))
        
        # Guardamos la información en sus respectivos ficheros, todos dentro de la carpeta usuarios. 
        carpeta = Path('usuarios')
        carpeta.mkdir(parents=True, exist_ok=True)    # Creamos, si no exsiste la carpeta.  
        
        # Almacenamos la información. 
        almacenar(f'{carpeta}/pub_{nombre}.txt', [n,e,int(pad)])
        almacenar(f'{carpeta}/priv_{nombre}.txt',[d])

        print(f'El usuario {nombre} se ha registrado con éxito. ')
    except ValueError as error:  
        print(f'{error}, los números introducidos no son correctos. ')