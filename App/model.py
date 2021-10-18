﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.chaininghashtable import keySet
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf
from datetime import datetime 
from DISClib.Algorithms.Sorting import shellsort
from datetime import timedelta



"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def initCatalog():
    catalog = mp.newMap(numelements=8,loadfactor=4)
    mp.put(catalog,"Artists",mp.newMap(numelements=4))
    mp.put(mp.get(catalog,"Artists")["value"],"id",mp.newMap(maptype="CHAINING",loadfactor=4))
    mp.put(mp.get(catalog,"Artists")["value"],"Año",mp.newMap(maptype="CHAINING",loadfactor=4))

    mp.put(catalog,"Artworks",mp.newMap(numelements=5,loadfactor=4))
    mp.put(mp.get(catalog,"Artworks")["value"],"Año_ad",mp.newMap(maptype="CHAINING",loadfactor=4))
    mp.put(mp.get(catalog,"Artworks")["value"],"Nacionalidad",mp.newMap(maptype="CHAINING",loadfactor=4))
    mp.put(mp.get(catalog,"Artworks")["value"],"Departamento",mp.newMap(maptype="CHAINING",loadfactor=4))
    mp.put(mp.get(catalog,"Artworks")["value"],"Medium",mp.newMap(maptype="CHAINING",loadfactor=4))

    return catalog

def addArtist(catalog,artist):
    artista = mp.newMap(numelements=8,loadfactor=4)
    mp.put(artista,"Const_id",artist["ConstituentID"].strip())
    mp.put(artista,"Nombre",artist["DisplayName"])
    mp.put(artista,"Año",int(artist["BeginDate"]))
    mp.put(artista,"Nacionalidad",artist["Nationality"].strip())
    mp.put(artista,"Fecha_falle",artist["EndDate"])
    mp.put(artista,"Genero",artist["Gender"])

    mp.put(artista,"Obras",mp.newMap(2,loadfactor=4))
    mp.put(mp.get(artista,"Obras")["value"],"Lista",lt.newList("ARRAY_LIST"))

    mp.put(mp.get(mp.get(catalog,"Artists")["value"],"id")["value"],mp.get(artista,"Const_id")["value"],artista)
    add_or_create_in_list(mp.get(mp.get(catalog,"Artists")["value"],"Año")["value"],mp.get(artista,"Año")["value"],artista)


def addArtwork(catalog,artwork):
    obra = mp.newMap(numelements=20)
    mp.put(obra,"id",artwork["ObjectID"])
    mp.put(obra,"Titulo",artwork["Title"])
    mp.put(obra,"Fecha",artwork["Date"])
    mp.put(obra,"Dimensiones",artwork["Dimensions"])
    mp.put(obra,"Clasificación",artwork["Classification"])
    mp.put(obra,"Departamento",artwork["Department"])

    if artwork["Medium"] == "":
        mp.put(obra,"Medio","*No especificado*")
    else:
        mp.put(obra,"Medio",artwork["Medium"])

    if artwork["DateAcquired"] != "":
        mp.put(obra,"Fecha_ad",datetime.strptime(artwork["DateAcquired"],"%Y-%m-%d"))
    else:
        mp.put(obra,"Fecha_ad",datetime.strptime("0001-01-01","%Y-%m-%d"))

    if artwork["CreditLine"] == "Purchase":
        mp.put(obra,"Compra",True)
    else:
        mp.put(obra,"Compra",False)

    artistas = artwork["ConstituentID"]
    artistas = artistas.replace("[","")
    artistas = artistas.replace("]","")
    artistas = artistas.split(",")

    mp.put(obra,"Artistas",lt.newList())
    nacionalidades = lt.newList()

    for codigo in artistas:
        codigo = codigo.strip()
        artista = mp.get(mp.get(mp.get(catalog,"Artists")["value"],"id")["value"],codigo)["value"]
        lt.addLast(mp.get(obra,"Artistas")["value"],artista)
        nacionalidad = mp.get(artista,"Nacionalidad")["value"]
        lt.addLast(mp.get(mp.get(artista,"Obras")["value"],"Lista")["value"],obra)
        add_or_create_in_list(mp.get(artista,"Obras")["value"],mp.get(obra,"Medio")["value"],obra)
        

        if lt.isPresent(nacionalidades,nacionalidad) == 0:
            lt.addLast(nacionalidades,nacionalidad)
            add_or_create_in_list(mp.get(mp.get(catalog,"Artworks")["value"],"Nacionalidad")["value"],nacionalidad,obra)

    add_or_create_in_list(mp.get(mp.get(catalog,"Artworks")["value"],"Año_ad")["value"],mp.get(obra,"Fecha_ad")["value"].year,obra)
    add_or_create_in_list(mp.get(mp.get(catalog,"Artworks")["value"],"Medium")["value"],mp.get(obra,"Medio")["value"],obra)
    


# Funciones para agregar informacion al catalogo

def add_or_create_in_list(mapa,llave,valor):
    if mp.contains(mapa,llave):
        lt.addLast(mp.get(mapa,llave)["value"],valor)
    else:
        mp.put(mapa,llave,lt.newList(datastructure="ARRAY_LIST"))
        lt.addLast(mp.get(mapa,llave)["value"],valor)

# Funciones para creacion de datos

# Funciones de consulta

def artistas_cronologico(catalog,anio_i,anio_f):
    datos = mp.get(mp.get(catalog,"Artists")["value"],"Año")["value"]
    años = mp.keySet(datos)

    años_rango = lt.newList("ARRAY_LIST")
    for año in lt.iterator(años):
        if año >= anio_i and año <= anio_f:
            lt.addLast(años_rango,año)
    
    shellsort.sort(años_rango,sort_years)

    lista_retorno = lt.newList("ARRAY_LIST")

    for año in lt.iterator(años_rango):
        lista_año = mp.get(datos,año)["value"]
        for artista in lt.iterator(lista_año):
            lt.addLast(lista_retorno,artista)

    return lista_retorno
        
def obras_por_nacionalidad(catalog):
    datos = mp.get(mp.get(catalog,"Artworks")["value"],"Nacionalidad")["value"]
    nacionalidades = mp.keySet(datos)

    lista_retorno = lt.newList("ARRAY_LLIST")

    for nacionalidad in lt.iterator(nacionalidades):
        if nacionalidad != "":
            mapa = mp.newMap(3)
            mp.put(mapa,"Nacionalidad",nacionalidad)
            mp.put(mapa,"Conteo",lt.size(mp.get(datos,nacionalidad)["value"]))
            mp.put(mapa,"Obras",mp.get(datos,nacionalidad)["value"].copy())

            lt.addLast(lista_retorno,mapa)
    
    shellsort.sort(lista_retorno,sort_nationalities_by_artworks)
    return lista_retorno

def adquisiciones_cronologico(fecha_i,fecha_f,catalog):
    datos = mp.get(mp.get(catalog,"Artworks")["value"],"Año_ad")["value"]
    años = mp.keySet(datos)

    rango_años = lt.newList("ARRAY_LIST")
    for año in lt.iterator(años):
        if año >= fecha_i.year and año <= fecha_f.year:
            lt.addLast(rango_años,año)
    
    shellsort.sort(rango_años,sort_years)

    lista_retorno = lt.newList("ARRAY_LIST")
    conteo_compras = 0

    if lt.size(rango_años) <= 8:
        for año in lt.iterator(rango_años):
            lista_año = mp.get(datos,año)["value"]
            shellsort.sort(lista_año,sort_ad_date)
            for obra in lt.iterator(lista_año):
                if mp.get(obra,"Fecha_ad")["value"] >= fecha_i and mp.get(obra,"Fecha_ad")["value"] <= fecha_f:
                    lt.addLast(lista_retorno,obra)
                    if mp.get(obra,"Compra")["value"]==True:
                        conteo_compras += 1
    
    else:
        for i in range(1,lt.size(rango_años)+1):
            if i in range(1,5) or i in range(lt.size(rango_años)-3,lt.size(rango_años)+1):
                año = lt.getElement(rango_años,i)
                lista_año = mp.get(datos,año)["value"]
                shellsort.sort(lista_año,sort_ad_date)
                for obra in lt.iterator(lista_año):
                    if mp.get(obra,"Fecha_ad")["value"] >= fecha_i and mp.get(obra,"Fecha_ad")["value"] <= fecha_f:
                        lt.addLast(lista_retorno,obra)
                        if mp.get(obra,"Compra")["value"]==True:
                            conteo_compras += 1
            else:
                año = lt.getElement(rango_años,i)
                lista_año = mp.get(datos,año)["value"]
                for obra in lt.iterator(lista_año):
                    año = lt.getElement(rango_años,i)
                    lt.addLast(lista_retorno,obra)
                    if mp.get(obra,"Compra")["value"]==True:
                        conteo_compras += 1
            
    return lista_retorno,conteo_compras


def artistas_prolificos(catalog,anio_i,anio_f,numero):
    datos = mp.get(mp.get(catalog,"Artists")["value"],"Año")["value"]
    años = mp.keySet(datos)

    rango_años = lt.newList("ARRAY_LIST")
    for año in lt.iterator(años):
        if año >= anio_i and año <= anio_f:
            lt.addLast(rango_años,año)
    
    lista = lt.newList("ARRAY_LIST")

    for año in lt.iterator(rango_años):
        lista_año = mp.get(datos,año)["value"]
        for artista in lt.iterator(lista_año):
            diccionario = mp.newMap(5,loadfactor=4)
            mp.put(diccionario,"Artista",artista)
            mp.put(diccionario,"Total obras",lt.size(mp.get(mp.get(artista,"Obras")["value"],"Lista")["value"]))
            mp.put(diccionario,"Numero de medios",lt.size(mp.get(artista,"Obras")["value"])-1)

            medios = keySet(mp.get(artista,"Obras")["value"])
            mayor_medio = None
            mayor_numero = -1
            for medio in lt.iterator(medios):
                if medio != "Lista":
                    medio_prueba = mp.get(mp.get(artista,"Obras")["value"],medio)
                    if lt.size(medio_prueba["value"]) > mayor_numero:
                        mayor_numero = lt.size(medio_prueba["value"])
                        mayor_medio = medio
            
            mp.put(diccionario,"Mayor medio",mayor_medio)

            lt.addLast(lista,diccionario)
        
    shellsort.sort(lista,sort_artistas_prolificos)

    if numero < lt.size(lista):
        lista = lt.subList(lista,1,numero)
    return lista




# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def sort_date(artwork1,artwork2):
    if mp.get(artwork1,"Fecha")["value"] < mp.get(artwork2,"Fecha")["value"]:
        return True
    else:
        return False

def sort_ad_date(artwork1,artwork2):
    if mp.get(artwork1,"Fecha_ad")["value"] < mp.get(artwork2,"Fecha_ad")["value"]:
        return True
    else:
        return False

def sort_years(año1,año2):
    if año1<año2:
        return True
    else:
        return False

def sort_years_datetime(año1,año2):
    if año1.year()<año2.year():
        return True
    else:
        return False

def sort_nationalities_by_artworks(nationality1,nationality2):
    if mp.get(nationality1,"Conteo")["value"] > mp.get(nationality2,"Conteo")["value"]:
        return True
    else:
        return False

def sort_artistas_prolificos(artista1,artista2):
    if mp.get(artista1,"Total obras")["value"]>mp.get(artista2,"Total obras")["value"]:
        return True
    elif mp.get(artista1,"Total obras")["value"]==mp.get(artista2,"Total obras")["value"] and mp.get(artista1,"Numero de medios")["value"] > mp.get(artista2,"Numero de medios")["value"]:
        return True
    elif mp.get(artista1,"Total obras")["value"]==mp.get(artista2,"Total obras")["value"] and mp.get(artista1,"Numero de medios")["value"] == mp.get(artista2,"Numero de medios"):
        return True
    else:
        return False
    
#Funciones de busqueda

def binary_search(arr, low, high, x):
    #Tomado y modificado de https://www.geeksforgeeks.org/python-program-for-binary-search/
    #Está pensada solamente para buscar el inicio de un rango.
 
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        prueba = lt.getElement(arr,mid)
        if lt.getElement(arr,mid) == x:
            #Revisar si hay duplicados
            while lt.getElement(arr,mid) == lt.getElement(arr,mid-1):
                mid -= 1
            return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif lt.getElement(arr,mid) > x:
            return binary_search(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return -1




    
        