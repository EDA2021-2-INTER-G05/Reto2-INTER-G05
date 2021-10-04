"""
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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from datetime import datetime 
from DISClib.Algorithms.Sorting import shellsort

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def initCatalog():
    catalog = mp.newMap(numelements=2)
    mp.put(catalog,"Artists",mp.newMap(numelements=3))
    mp.put(mp.get(catalog,"Artists")["value"],"id",mp.newMap())
    mp.put(mp.get(catalog,"Artists")["value"],"Año",mp.newMap())

    mp.put(catalog,"Artworks",mp.newMap(numelements=5))
    mp.put(mp.get(catalog,"Artworks")["value"],"Año_ad",mp.newMap())
    mp.put(mp.get(catalog,"Artworks")["value"],"Nacionalidad",mp.newMap())
    mp.put(mp.get(catalog,"Artworks")["value"],"Departamento",mp.newMap())
    mp.put(mp.get(catalog,"Artworks")["value"],"Medium",mp.newMap())

    return catalog

def addArtist(catalog,artist):
    artista = mp.newMap(numelements=8)
    mp.put(artista,"Const_id",artist["ConstituentID"].strip())
    mp.put(artista,"Nombre",artist["DisplayName"])
    mp.put(artista,"Año",int(artist["BeginDate"]))
    mp.put(artista,"Nacionalidad",artist["Nationality"].strip())

    mp.put(mp.get(mp.get(catalog,"Artists")["value"],"id")["value"],mp.get(artista,"Const_id")["value"],artista)
    add_or_create_in_list(mp.get(mp.get(catalog,"Artists")["value"],"Año")["value"],mp.get(artista,"Año")["value"],artista)


def addArtwork(catalog,artwork):
    obra = mp.newMap(numelements=20)
    mp.put(obra,"id",artwork["ObjectID"])
    mp.put(obra,"Titulo",artwork["Title"])
    mp.put(obra,"Medio",artwork["Medium"])
    mp.put(obra,"Fecha",artwork["Date"])

    if artwork["DateAcquired"] != "":
        mp.put(obra,"Fecha_ad",datetime.strptime(artwork["DateAcquired"],"%Y-%m-%d"))
    else:
        mp.put(obra,"Fecha_ad",datetime.strptime("0001-01-01","%Y-%m-%d"))

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
        mp.put(mapa,llave,lt.newList())
        lt.addLast(mp.get(mapa,llave)["value"],valor)

# Funciones para creacion de datos

# Funciones de consulta

def obras_antiguas_medio(catalog,medio,numero):

    datos = mp.get(mp.get(catalog,"Artworks")["value"],"Medium")["value"]
    lista = mp.get(datos,medio)["value"]
    shellsort.sort(lista,sort_date)

    if lt.size(lista)<numero:
        numero = lt.size(lista)
    i = 1
    retorno = lt.newList("ARRAY_LIST")
    while True:
        if mp.get(lt.getElement(lista,i),"Fecha")["value"] != "":
            lt.addLast(retorno,lt.getElement(lista,i))
            i += 1
        if i == numero+1:
            break
    return retorno

def numero_obras_nacionalidad(catalog,nacionalidad):
    numero = lt.size(mp.get(mp.get(mp.get(catalog,"Artworks")["value"],"Nacionalidad")["value"],nacionalidad)["value"])
    return numero

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def sort_date(artwork1,artwork2):
    if mp.get(artwork1,"Fecha")["value"] < mp.get(artwork2,"Fecha")["value"]:
        return True
    else:
        return False
    


    
        