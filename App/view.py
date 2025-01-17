﻿"""
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

from typing import List
from prettytable import prettytable
from prettytable.prettytable import ALL, HEADER
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
import time
from prettytable import PrettyTable
from datetime import datetime

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

catalog2 = None
def obtener_nombres_artistas(obra):
    artistas = mp.get(obra,"Artistas")["value"]
    lista = []
    for artista in lt.iterator(artistas):
        lista.append(mp.get(artista,"Nombre")["value"])
    return lista



def print_artistas_cronologico(resultado,tiempo):
    print("Hay un total de " + str(lt.size(resultado)) + " artistas en el rango.")
    print("Se muestra a continuación los 3 primeros y los 3 últimos:")

    tabla = PrettyTable()
    tabla.field_names = ["Nombre","Año de nacimiento","Año de fallecimiento","Nacionaliad","Genero"]
    
    for i in range(1,4):
        artista = lt.getElement(resultado,i)
        tabla.add_row([mp.get(artista,"Nombre")["value"],mp.get(artista,"Año")["value"],mp.get(artista,"Fecha_falle")["value"],mp.get(artista,"Nacionalidad")["value"],mp.get(artista,"Genero")["value"]])
    
    for i in range(lt.size(resultado)-2,lt.size(resultado)+1):
        artista = lt.getElement(resultado,i)
        tabla.add_row([mp.get(artista,"Nombre")["value"],mp.get(artista,"Año")["value"],mp.get(artista,"Fecha_falle")["value"],mp.get(artista,"Nacionalidad")["value"],mp.get(artista,"Genero")["value"]])

    print(tabla)
    print("Tiempo requerido: " + str(tiempo) + " msg")


def print_numero_obras_nacionaliad(resultado,tiempo):

    tabla = PrettyTable()
    tabla.field_names=["Nacionalidad","Número de obras"]
    for i in range(1,11):
        nacionalidad = lt.getElement(resultado,i)
        tabla.add_row([mp.get(nacionalidad,"Nacionalidad")["value"],mp.get(nacionalidad,"Conteo")["value"]])

    print("El top 10 de nacionalidades con más obras es:")
    print(tabla)

    print("Muestra de las lista de la nacionalidad con mayor cantidad de obras:")
    tabla2 =PrettyTable(hrules = ALL)
    tabla2.field_names = ["Titulo","Artista(s)","Fecha","Medio","Dimensiones"]
    tabla2.max_width = 40
    
    lista = mp.get(lt.getElement(resultado,1),"Obras")["value"]
    for i in range(1,4):
        obra = lt.getElement(lista,i)
        nombre_artistas = obtener_nombres_artistas(obra)
        tabla2.add_row([mp.get(obra,"Titulo")["value"],nombre_artistas,mp.get(obra,"Fecha")["value"],mp.get(obra,"Medio")["value"],mp.get(obra,"Dimensiones")["value"]])

    for i in range(lt.size(lista)-2,lt.size(lista)+1):
        obra = lt.getElement(lista,i)
        nombre_artistas = obtener_nombres_artistas(obra)
        tabla2.add_row([mp.get(obra,"Titulo")["value"],nombre_artistas,mp.get(obra,"Fecha")["value"],mp.get(obra,"Medio")["value"],mp.get(obra,"Dimensiones")["value"]])
    
    print(tabla2)
    print("Tiempo requerido: " + str(tiempo) + " msg")

def printAdquisicionesCronologicas(lista,conteo,tiempo):
    print("La cantidad de obras en el rango es " + str(lt.size(lista)))
    print("De estas, " + str(conteo) + " fueron compradas.")
    tabla2 =PrettyTable(hrules = ALL)

    tabla2.field_names = ["Titulo","Artista(s)","Fecha","Fecha ad","Medio","Dimensiones"]
    tabla2.max_width = 30
    
    for i in range(1,4):
        obra = lt.getElement(lista,i)
        nombre_artistas = obtener_nombres_artistas(obra)
        tabla2.add_row([mp.get(obra,"Titulo")["value"],nombre_artistas,mp.get(obra,"Fecha")["value"],mp.get(obra,"Fecha_ad")["value"],mp.get(obra,"Medio")["value"],mp.get(obra,"Dimensiones")["value"]])

    for i in range(lt.size(lista)-2,lt.size(lista)+1):
        obra = lt.getElement(lista,i)
        nombre_artistas = obtener_nombres_artistas(obra)
        tabla2.add_row([mp.get(obra,"Titulo")["value"],nombre_artistas,mp.get(obra,"Fecha")["value"],mp.get(obra,"Fecha_ad")["value"],mp.get(obra,"Medio")["value"],mp.get(obra,"Dimensiones")["value"]])
    
    print(tabla2)
    print("Tiempo requerido: " + str(tiempo) + " msg")

def print_artistas_prolificos(resultado,tiempo):
    tabla = PrettyTable()
    tabla.field_names =["Nombre","Fecha Nacimiento","Genero","Total Obras","Total Técnicas","Técnica más utilizada"]
    for diccionario in lt.iterator(resultado):
        artista = mp.get(diccionario,"Artista")["value"]
        tabla.add_row([mp.get(artista,"Nombre")["value"],mp.get(artista,"Año")["value"],mp.get(artista,"Genero")["value"],mp.get(diccionario,"Total obras")["value"],mp.get(diccionario,"Numero de medios")["value"],mp.get(diccionario,"Mayor medio")["value"]])
    print("Los artistas más prolificos del museo en ese rango son los siguientes: ")
    print(tabla)

    tabla2= PrettyTable(hrules = ALL)
    tabla2.field_names = ["Titulo","Fecha","Fecha adquisición","Medio","Departamento","Clasificación","Dimensiones"]
    mayor_medio = mp.get(lt.getElement(resultado,1),"Mayor medio")["value"]
    lista_obras = mp.get(mp.get(mp.get(lt.getElement(resultado,1),"Artista")["value"],"Obras")["value"],mayor_medio)["value"]
    
    if lt.size(lista_obras)<6:
        for i in range(1,lt.size(lista_obras)+1):
            obra = lt.getElement(lista_obras,i)
            tabla2.add_row([mp.get(obra,"Titulo")["value"],mp.get(obra,"Fecha")["value"],mp.get(obra,"Fecha_ad")["value"],mp.get(obra,"Medio")["value"],mp.get(obra,"Departamento")["value"],mp.get(obra,"Clasificación")["value"],mp.get(obra,"Dimensiones")["value"]])
    else:

        for i in range(1,6):
            obra = lt.getElement(lista_obras,i)
            tabla2.add_row([mp.get(obra,"Titulo")["value"],mp.get(obra,"Fecha")["value"],mp.get(obra,"Fecha_ad")["value"],mp.get(obra,"Medio")["value"],mp.get(obra,"Departamento")["value"],mp.get(obra,"Clasificación")["value"],mp.get(obra,"Dimensiones")["value"]])
    print("Las 5 primeras obras del medio más utilizado del artista más prolífico son las siguientes: ")
    tabla2.max_width = 25
    print(tabla2)
    print("Tiempo requerido: " + str(tiempo) + " msg")



def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    return controller.loadData(catalog)


def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Listar cronnológicamente artistas")
    print("2- Listar cronológicamente las adquisiciones")
    print("3- clasificar tecnicas de un artista")
    print("4- Clasificar obras por nacionalidad de sus creadores")
    print("5- transportar obras por departamento")
    print("6 - Encontrar los artistas más prolificos del museo")

def initCatalog2():
    return controller.initCatalog2()

def loadData2(catalog2):
    controller.loadData2(catalog2)

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
        catalog2 = initCatalog2()
        loadData(catalog)
        loadData2(catalog2)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Se han cargado los datos exitosamente.")
        print("Tiempo requerido: "+ str(elapsed_time_mseg) + " mseg")

    elif int(inputs[0]) == 1:
        anio_i = int(input("Ingrese el año inicial: "))
        anio_f = int(input("Ingrese el año final: "))
        print("Cargando información...")
        start_time = time.process_time()
        resultado = controller.artistas_cronologico(catalog,anio_i,anio_f)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_artistas_cronologico(resultado,elapsed_time_mseg)

    
    elif int(inputs[0]) == 2:
        fecha_i = input("Ingrese la fecha inicial (YYYY-MM-DD): ")
        fecha_i = fecha_i.strip()
        fecha_i = datetime.strptime(fecha_i,"%Y-%m-%d")
        fecha_f = input("Ingrese la fecha final (YYYY-MM-DD): ")
        fecha_f = fecha_f.strip()
        fecha_f = datetime.strptime(fecha_f,"%Y-%m-%d")
        print("Cargando información de los archivos...")
        start_time = time.process_time()
        resultado = controller.adquisiciones_cronologico(fecha_i,fecha_f,catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        printAdquisicionesCronologicas(resultado[0],resultado[1],elapsed_time_mseg)

    elif int(inputs[0]) == 3: 
        artist =  input("Ingrese artista a buscar: ")
        start_time = time.process_time()
        mas = controller.artista_medio(catalog2, artist)
        size = mp.size(mas[1])
        top = controller.med5(mas[1])
        final = controller.llaves(top)
        stop_time = time.process_time()
        c = 0
        while c < 10:
            a = str(final[1]["elements"][c])
            b = str(final[1]["elements"][c+1])
            print(a.center(50)+"|"+b.center(9))
            print("-"*60)
            c+=2      
        
        a = str(final[1]["elements"][0])
        med = controller.final(catalog2, mas[0],a) 
        print("El tiempo de carga fue de:",str(elapsed_time_mseg), "s")
        print(str(artist) + " con ID " + str(mas[0]) + " tiene  " + str(size) + " obras")      
        print("Tiene 5" + str(final[0]) + " medios")
        print("Medio".center(50)+"|"+"Obras".center(9))
        print("-"*30)


    elif int(inputs[0]) == 4:
        print("Cargando información...")
        start_time = time.process_time()
        resultado = controller.obras_por_nacionalidad(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_numero_obras_nacionaliad(resultado,elapsed_time_mseg)

    elif int(inputs[0]) == 5:
        department = input("Digite el departamento a evaluar: ")
        start_time = time.process_time()
        respuesta = controller.reglas_transporte(catalog2,department)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("El tiempo para cargar los archivos fue de:", str(elapsed_time_mseg) , "s") 
        print ("Las medidas del departamento son " + str(respuesta[0]) + " obras.")
        print ("El costo total es " + str(respuesta[1]) + "USD")
        print("obras mas caras:")
        print ("=" * 50)
        for a in lt.iterator(respuesta[2]):
            print("ID: " + a["ObjectID"])
            print("titulo: " + a["Title"])
            print("nombre: ")
            F = a["ConstituentID"].split(",")
            for artista in F: 
                artista = artista.strip("[] ")
                print(mp.get(catalog2["ConstituentName"], artista)["value"])
            print("medio: " + a["Medium"])
            print("fecha: " + a["Date"])
            print("dimensiones: " + a["Dimensions"])
            print("puesto: " + a["Classification"] )
            print("Costo" + str(a["Costo"]))
            print("url: " + a["URL"])
            print ("=" * 50)
        print ("obras mas antiguas: ")
        print ("=" * 50)
        for b in lt.iterator(respuesta[3]):
            print("ID: " + b["ObjectID"])
            print("Titulo: " + b["Title"])
            print("nombre: ")
            F = b["ConstituentID"].split(",")
            for artista in F: 
                artista = artista.strip("[] ")
                print(mp.get(catalog2["ConstituentName"], artista)["value"])
            print("medio: " + b["Medium"])
            print("fecha: " + b["Date"])
            print("dimensiones: " + b["Dimensions"])
            print("puesto: " + b["Classification"] )
            print("costo" + str(b["Costo"]))
            print("url: " + b["URL"])
            print ("=" * 50)
    elif int(inputs[0]) == 6:
        anio_i = int(input("Ingrese el año inicial: "))
        anio_f = int(input("Ingrese el año final: "))
        numero = int(input("Ingrese cúantos de los artístas más prolíficos desea ver: "))
        print("Cargando información de los archivos...")
        start_time = time.process_time()
        resultado = controller.artistas_prolificos(catalog,anio_i,anio_f,numero)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_artistas_prolificos(resultado,elapsed_time_mseg)

    else:
        sys.exit(0)
sys.exit(0)
