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
 """

import config as cf
import model
import csv
from DISClib.Algorithms.Sorting import shellsort
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def initCatalog():
    catalog = model.initCatalog()
    return catalog

def loadData(catalog):
    loadArtist(catalog)
    loadArtworks(catalog)

def loadArtist(catalog):

    Artistfile = cf.data_dir + 'Artists-utf8-large.csv'
    input_file = csv.DictReader(open(Artistfile, encoding='utf-8'))
    for Artist in input_file:
        model.addArtist(catalog, Artist)

def loadArtworks(catalog):
    Artworks = cf.data_dir + 'Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(Artworks, encoding='utf-8'))
    for Artwork in input_file:
        model.addArtwork(catalog, Artwork)

def obras_antiguas_medio(datos,medio,numero):
    lista = mp.get(datos,medio)["value"]
    shellsort.sort(lista,model.sort_date)

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
    
    

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
