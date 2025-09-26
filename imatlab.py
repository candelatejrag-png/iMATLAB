# Importamos las librerías necesarias:
import sys

# importamos los scripts necesarios: 
import modular2 as f
import errores as e

# Implementamos las funciones que van a ser empleadas en el programa: 
def run_commands(fin, fout): 
    pass

if __name__ == '__main__': 

    # Creamos un diccionario donde la clave es la función que pide el usuario y su valor asociado es una lista formada por la función de modular.py asociada al comando y el número de argumentos que recibe la función. 
    dic_comandos = {'primo': 'es_primo','primos': 'lista_primos', 'factorizar': 'factorizar', 'mcd': 'mcd', 'coprimos': 'coprimos', 'pow': 'potencia_mod_p', 'inv': 'inversa_mod_p', 'euler': 'euler', 'legendre': 'legendre', 'resolversistema': 'resolver_sistema_congruencias'}

    if len(sys.argv) != 0:
        pass
    else: 
        # LEEMOS EL FICHERO Y LO PROCESAMOS COMO SI FUERAN COMANDOS Y LOS ALMACENA EN OTRO FICHERO CON LAS SOLUCIONES. 
        pass 
    