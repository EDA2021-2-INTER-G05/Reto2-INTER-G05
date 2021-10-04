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

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def print_n_obras_antigua(lista):
    for obra in lt.iterator(lista):
        print(mp.get(obra,"Titulo")["value"],mp.get(obra,"Fecha")["value"])

def print_numero_obras_nacionaliad(resultado):
    print("El número de obras con esa nacionalidad es: ",resultado)

def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    return controller.loadData(catalog)

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- n obras más antiguas de un medio")
    print("3 - Número total de obras de una nacionaliad")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print("Se han cargado los datos exitosamente.")

    elif int(inputs[0]) == 2:
        medio = input("Seleccione el medio: ")
        medio = medio.strip()
        numero = int(input("Ingrese la cantidad de obras: "))
        lista = controller.obras_antiguas_medio(catalog,medio,numero)
        print_n_obras_antigua(lista)
    
    elif int(inputs[0]) == 3:
        nacionalidad = input("Ingrese la nacionalidad: ").strip()
        resultado = controller.numero_obras_nacionalidad(catalog,nacionalidad)
        print_numero_obras_nacionaliad(resultado)

    else:
        sys.exit(0)
sys.exit(0)
