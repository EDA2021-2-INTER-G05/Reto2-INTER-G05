"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
import time

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def print_n_obras_antigua(lista,tiempo):
    for obra in lt.iterator(lista):
        print(mp.get(obra,"Titulo")["value"],mp.get(obra,"Fecha")["value"])
    
    print("Tiempo requerido: " + str(tiempo) + " msg")

def print_numero_obras_nacionaliad(resultado,tiempo):
    print("El número de obras con esa nacionalidad es: ",resultado)
    print("Tiempo requerido: " + str(tiempo) + " msg")

def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    return controller.loadData(catalog)

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- n obras más antiguas de un medio")
    print("2 - Número total de obras de una nacionaliad")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        start_time = time.process_time()
        catalog = initCatalog()
        loadData(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Se han cargado los datos exitosamente.")
        print("Tiempo requerido: "+ str(elapsed_time_mseg) + " mseg")

    elif int(inputs[0]) == 1:
        medio = input("Seleccione el medio: ")
        medio = medio.strip()
        numero = int(input("Ingrese la cantidad de obras: "))
        start_time = time.process_time()
        lista = controller.obras_antiguas_medio(catalog,medio,numero)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_n_obras_antigua(lista,elapsed_time_mseg)
    
    elif int(inputs[0]) == 2:
        nacionalidad = input("Ingrese la nacionalidad: ").strip()
        start_time = time.process_time()
        resultado = controller.numero_obras_nacionalidad(catalog,nacionalidad)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_numero_obras_nacionaliad(resultado,elapsed_time_mseg)

    else:
        sys.exit(0)
sys.exit(0)
