# Importamos los ficheros necesarios. 
import rsa as f

# Importamos las librerías necesarias. 
import sys
from pathlib import Path

# Creamos un error específico para gestionar los problemas de lectura y exsistencia de ficheros. 
class LecturaError(Exception): 
    pass

# Creamos las funciones necesarias para el desarrollo del programa. 

def extraer_clave(nombre_fichero: str)-> list[int]: 
    '''Función que toma el nombre del fichero que se desea leer y extrae la información almacenandola en una lista (datos) que se devolverá después. 
    
    Args: 
        nombre_fichero (str): el nombre del fichero que se desea leer. 
    Returns: 
        datos (list[int]): lista con los datos que buscamos, las claves públicas o privadas del usuario ya pasadas a formato numérico. 
    Raises: 
        LecturaError (Exception): si el fichero no se encuentra se lanza un error avisando de que el usuario no esta registrado en la base de datos. 
    '''
    try: 
        with open(f'usuarios/{nombre_fichero}.txt','r',encoding='utf-8') as fi: 
            datos = [int(linea.strip()) for linea in fi]
        return datos if len(datos) > 1 else datos[0]
    except FileNotFoundError: 
        raise LecturaError(f'no se ha encontrado el archivo asociado al usuario {nombre_fichero}. Asegurese de que dicho usuario este registrado. ')

def ac_cifrar(n: int, e: int, pad: int): 
    '''Función que ejecuta una le las acciones del programa, pide que el usuario introduzca un mensaje por pantalla y empleando las funciones auxiliares
    del módulo rsa.py y los argumentos recibimos por pantalla cifra ese mensaje imprimiendo el nuevo mensaje cifrado. 
    
    Args: 
        n (int): parte de la clave pública del usuario al que se le quiere mandar el mensaje (el módulo en la operación a realizar). 
        e (int): parte de la clave pública del usuario al que se le quiere mandar el mensaje (el exponente en la operación a realizar). 
        pad (int): el número de cifras de padding previamente escojido por el usuario receptor del mensaje que debe incluir la cadena solución. 
    Returns: 
        None. 
    Raises: 
        None. 
    '''
    mensaje = input('introduzca el texto que desea cifrar: ')
    m_cifrado = f.cifrar_cadena_rsa(mensaje,n,e,pad)
    print(str(m_cifrado)[1:-1])

def ac_descifrar(n: int, d: int, pad: int): 
    m_cifrado = input('Introduzca mensaje que desea descifrar: ')
    try:
        mensaje = f.descifrar_cadena_rsa(map(int,m_cifrado.split(' ')),n,d,pad)
        print(mensaje)
    except ValueError as error: 
        print(f'el mensaje no se ha podido descodificar con éxito ya que {error}')

def main(usuario1: str, usuario2: str): 
    '''Función encargada de realizar el programa principal de chriptochat.py. 
    
    args: 
        usuario1 (str): el que abre la interfaz para comunicarse o leer mensajes de otro usuario. 
        usuario2 (str): el usuario con el que se quiere comunicar usuario1, el que recibirá un mensaje cifrado o del que se descodificará
        un mensaje. 
    Raises: 
        None
    '''
    # Extraemos las claves publicas y privadas de usuario1 y las claves púclicas de usuario2 si estos exsisten, sino gestionamos el error. 
    try:
        n1, e1, pad1 = extraer_clave(f'pub_{usuario1}')
        d1 = extraer_clave(f'priv_{usuario1}')
        n2,e2,pad2 = extraer_clave(f'pub_{usuario2}')

        # Abrimos el chat: 
        accion = input('Introduzca la acción a realizar: cifrar (C), descifrar (D) o salir (S): ').upper()
        while accion != salir: 
            if accion == cifrar: 
                ac_cifrar(n2,e2,pad2)
            elif accion == descifrar: 
                ac_descifrar(n1,d1,pad1)
            else: 
                print('Esta acción no esta disponible, vuelva a intentarlo. ')
            accion = input('Introduzca la acción a realizar: cifrar (C), descifrar (D) o salir (S): ').upper()
    except LecturaError as error: 
        print(error)

if __name__ == '__main__': 

    # Creamos las variables mecesarias. 
    cifrar = 'C'
    descifrar = 'D'
    salir = 'S'

    # Validamos y guardamos el nombre de los usuarios involucrados en el chat.
    if len(sys.argv) == 3:
        main(sys.argv[1],sys.argv[2])
    else: 
        print(f'No se ha introducido un número de usuarios adecuado. se deben introducir 2 nombres de usuario cuándo se han introducido {len(sys.argv)}. ')
    
    print('se ha salido del programa. ')