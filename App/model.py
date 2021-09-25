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

def addArtist(catalog,artist):
    artista = mp.newMap()
    mp.put(artista,"Const_id",int(artist["ConstituentID"]))
    mp.put(artista,"Nombre",artist["DisplayName"])

    lt.addLast(mp.get(catalog,"Artists")["value"],artista)

def addArtwork(catalog,artwork):
    artwork = mp.newMap()
    mp.put(artwork,"id",artwork["ObjectID"])
    mp.put(artwork,"Titulo",artwork["Title"])
    mp.put(artwork,"Medio",artwork["Medium"])
    mp.put(artwork,"Fecha",artwork["Date"])

    lt.addLast(mp.get(catalog,"Artworks")["value"],artwork)

    medio = mp.get(mp.get(catalog,"Medium"),artwork["Medium"])
    if medio:
        lt.addLast()

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
