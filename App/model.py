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

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def initCatalog():
    catalog = mp.newMap()
    mp.put(catalog,"Artists",lt.newList("ARRAY_LIST"))
    mp.put(catalog,"Artworks",lt.newList("ARRAY_LIST"))
    mp.put(catalog,"Medium",mp.newMap())
    return catalog

def addArtist(catalog,artist):
    artista = mp.newMap()
    mp.put(artista,"Const_id",int(artist["ConstituentID"]))
    mp.put(artista,"Nombre",artist["DisplayName"])

    prueba = mp.get(catalog,"Artists")

    lt.addLast(mp.get(catalog,"Artists")["value"],artista)

def addArtwork(catalog,artwork):
    obra = mp.newMap()
    mp.put(obra,"id",artwork["ObjectID"])
    mp.put(obra,"Titulo",artwork["Title"])
    mp.put(obra,"Medio",artwork["Medium"])
    mp.put(obra,"Fecha",artwork["Date"])

    lt.addLast(mp.get(catalog,"Artworks")["value"],artwork)

    medio = mp.get(mp.get(catalog,"Medium")["value"],mp.get(obra,"Medio")["value"])
    if medio:
        lt.addLast(mp.get(mp.get(catalog,"Medium")["value"],medio["key"])["value"],obra)
    else: 
        mp.put(mp.get(catalog,"Medium")["value"],artwork["Medium"],lt.newList("ARRAY_LIST"))

        

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def sort_date(artwork1,artwork2):
    if mp.get(artwork1,"Fecha")["value"] < mp.get(artwork2,"Fecha")["value"]:
        return True
    else:
        return False
    
