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
        return datos
    except FileNotFoundError: 
        raise LecturaError(f'no se ha encontrado el archivo asociado al usuario {nombre_fichero}. Asegurese de que dicho usuario este registrado. ')

def ac_cifrar(n: int, e: int, pad: int): 
    mensaje = input('introduzca el texto que desea cifrar: ')
    m_cifrado = f.cifrar_cadena_rsa(mensaje,n,e,pad)
    print(m_cifrado)

def ac_descifrar(d: int, pad: int): 
    m_cifrado = input('Introduzca mensaje que desea descifrar: ')
    mensaje = f.descifrar_cadena_rsa(m_cifrado.split(' '))
    print(mensaje)


if __name__ == '__main__': 

    # Creamos las variables mecesarias. 
    cifrar = 'C'
    descifrar = 'D'
    salir = 'S'

    # Guardamos el nombre de los usuarios involucrados en el chat.
    usuario1,usuario2 = sys.argv[1],sys.argv[2]
    
    # Extraemos las claves publicas y privadas de usuario1 y las claves púclicas de usuario2 si estos exsisten, sino gestionamos el error. 
    try:
        n1, e1, pad1 = extraer_clave(f'pub_{usuario1}')
        d1 = extraer_clave(f'priv_{usuario1}')
        n2,e2,pad2 = extraer_clave(f'pub_{usuario2}')

        # Abrimos el chat: 
        accion = input('Introduzca la acción a realizar: cifrar (C), descifrar (D) o salir (S)').upper()
        while accion != salir: 
            if accion == cifrar: 
                ac_cifrar(n2,e2,pad2)
            elif accion == descifrar: 
                ac_descifrar()
            else: 
                print('Esta acción no esta disponible, vuelva a intentarlo. ')
            accion = input('Introduzca la acción a realizar: cifrar (C), descifrar (D) o salir (S): ').upper()
    except LecturaError as error: 
        print(error)
    
    print('se ha salido del programa. ')