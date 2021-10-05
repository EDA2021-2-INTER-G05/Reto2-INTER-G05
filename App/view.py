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
from prettytable import PrettyTable

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def print_artistas_cronologico(resultado,tiempo):
    print("Hay un total de " + str(lt.size(resultado)) + " artistas en el rango.")
    print("Se muestra a continuación los 3 primeros y los 3 últimos:")

    tabla = PrettyTable()
    tabla.field_names = ["Nombre","Año de nacimiento","Año de fallecimiento","Nacionaliad","Genero"]
    
    for i in range(1,4):
        artista = lt.getElement(resultado,i)
        tabla.add_row([mp.get(artista,"Nombre")["value"],mp.get(artista,"Año")["value"],mp.get(artista,"Fecha_falle")["value"],mp.get(artista,"Nacionalidad")["value"],mp.get(artista,"Genero")["value"]])
    
    for i in range(lt.size(resultado)-3,lt.size(resultado)):
        artista = lt.getElement(resultado,i)
        tabla.add_row([mp.get(artista,"Nombre")["value"],mp.get(artista,"Año")["value"],mp.get(artista,"Fecha_falle")["value"],mp.get(artista,"Nacionalidad")["value"],mp.get(artista,"Genero")["value"]])

    print(tabla)
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
    print("1- Listar cronnológicamente artistas")
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
        anio_i = int(input("Ingrese el año inicial: "))
        anio_f = int(input("Ingrese el año final: "))
        start_time = time.process_time()
        resultado = controller.artistas_cronologico(catalog,anio_i,anio_f)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_artistas_cronologico(resultado,elapsed_time_mseg)

    
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
