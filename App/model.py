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


from DISClib.DataStructures.chaininghashtable import keySet
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import mergesort as ms
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
    mp.put(mp.get(catalog,"Artists")["value"],"Nombres",mp.newMap(maptype="CHAINING",loadfactor=4))

    mp.put(catalog,"Artworks",mp.newMap(numelements=6,loadfactor=4))
    mp.put(mp.get(catalog,"Artworks")["value"],"Año_ad",mp.newMap(maptype="CHAINING",loadfactor=4))
    mp.put(mp.get(catalog,"Artworks")["value"],"Nacionalidad",mp.newMap(maptype="CHAINING",loadfactor=4))
    mp.put(mp.get(catalog,"Artworks")["value"],"Departamento",mp.newMap(maptype="CHAINING",loadfactor=4))
    mp.put(mp.get(catalog,"Artworks")["value"],"Medium",mp.newMap(maptype="CHAINING",loadfactor=4))

    return catalog

def newCatalog2():
    catalog2 = {'artists': None,
               'artworks': None,
               }
    catalog2["artworks"] = mp.newMap(numelements = 3000, maptype="PROBING", loadfactor= 0.75 ) 
    catalog2["Mediumar"]= mp.newMap(numelements=1667, maptype="PROBING", loadfactor= 0.5)
    catalog2["ids"] = mp.newMap(numelements=2000, maptype="PROBING", loadfactor= 0.5)
    catalog2["Department"] = mp.newMap(numelements=23, maptype= "PROBING", loadfactor= 0.5) 
    catalog2["ConstituentName"] = mp.newMap(numelements=3907, maptype="PROBING", loadfactor= 0.5) 
    
    return catalog2

def addArtworks(catalog2, artwork):   
    lista = artwork["ConstituentID"].strip("[]")  
    lista = lista.replace(" ","")
    lista = lista.split(",")   
    for a in lista:     
        esta = mp.contains(catalog2["artworks"], int(a))
        if esta:
            b = mp.get(catalog2["artworks"],int(a))["value"]
            lt.addLast(b, artwork)
            mp.put(catalog2["artworks"],int(a),b)
        else:
            b = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(b, artwork)
            mp.put(catalog2["artworks"], int(a),b)      

  
def ids(catalog2, artist):
    mp.put(catalog2["ids"], artist["DisplayName"], int(artist["ConstituentID"]))

def medium(catalog2, artworks):
    ids = artworks["ConstituentID"].strip("[]")
    ids = ids.split(",")
    for a in ids:
        a = a.strip()
        esta = mp.contains(catalog2["Mediumar"], int(a))
        if not esta:
            lista = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lista, artworks["Medium"])
            mp.put(catalog2["Mediumar"], int(a),lista)
        else:
            lista = mp.get(catalog2["Mediumar"], int(a))["value"]
            lt.addLast(lista,artworks["Medium"])
            mp.put(catalog2["Mediumar"], int(a), lista)

def Department(catalog2, artwork):  
    encontrar = mp.contains(catalog2["Department"], artwork["Department"])
    if not encontrar:
        if artwork["Department"] != "" and artwork["Department"] != None:
            nuevo = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(nuevo, artwork)
            mp.put(catalog2["Department"], artwork["Department"], nuevo)
    else:
        nuevo = mp.get(catalog2["Department"], artwork["Department"])["value"]
        lt.addLast(nuevo, artwork)
        mp.put(catalog2["Department"], artwork["Department"], nuevo)

def name (catalog2, artist):
    mp.put(catalog2["ConstituentName"],artist["ConstituentID"], artist["DisplayName"])


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
    mp.put(mp.get(mp.get(catalog,"Artists")["value"],"Nombres")["value"],mp.get(artista,"Nombre")["value"],artista)
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
    add_or_create_in_list(mp.get(mp.get(catalog,"Artworks")["value"],"Departamento")["value"],mp.get(obra,"Departamento")["value"],obra)
    


# Funciones para agregar informacion al catalogo

def add_or_create_in_list(mapa,llave,valor):
    if mp.contains(mapa,llave):
        lt.addLast(mp.get(mapa,llave)["value"],valor)
    else:
        mp.put(mapa,llave,lt.newList(datastructure="ARRAY_LIST"))
        lt.addLast(mp.get(mapa,llave)["value"],valor)

# Funciones para creacion de datos
def sort_medium(med1,med2):
    return med1 > med2
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
#req 3
def artista_medio(catalog2,artist):
    
    id = mp.get(catalog2["ids"], artist)["value"] 
   
    medium = mp.get(catalog2["Mediumar"], id)["value"]
    

    return(id,medium)
   
def med5(medios):
    map = mp.newMap(numelements=50, maptype="PROBING", loadfactor= 0.5)
    for a in lt.iterator(medios):
        esta = mp.contains(map, a)
        if not esta:
            count = 1
            mp.put(map, a,count)
        else:
            count = mp.get(map, a)["value"]
            count += 1
            mp.put(map, a,count)
    return map

def llaves(map):
    llaves = mp.keySet(map)
    valores = mp.valueSet(map)
    lista = lt.newList(datastructure="ARRAY_LIST")
    size = mp.size(llaves)
    sublist = lt.subList(valores, 0, size)
    final = ms.sort(sublist,sort_medium)
    for a in lt.iterator(final):
        
        func = lt.isPresent(valores, a)
        key = lt.getElement(llaves,func)
        lt.addLast(lista, key)
        lt.addLast(lista, a)

        lt.deleteElement(valores, func)
        lt.deleteElement(llaves, func)
    return (size, lista) 


def final(catalog2, id, med):
    obrass = mp.get(catalog2["artworks"],id)["value"]
    print(" ")
    print("+"+("-"*150)+"+")
    print("|" + "Title".center(105)+" | "+ "Date".center(13)+" | "+"Medium".center(15)+" | "+"Dimensions".center(74)+" | ")
    print("+"+("-"*217)+"+")
    for i in lt.iterator(obrass):
        if i["Medium"] == med:
           
            print("|"+i["Title"].center(105)+" | "+ i["Date"].center(13)+" | "+i["Medium"].center(15)+" | "+i["Dimensions"].center(74)+" | ")
            print("+"+("-"*217)+"+")
   
#fin req 3
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
#req 5
def reglas_transporte(catalog2, department):
    lista1 = mp.get(catalog2["Department"], department)["value"]
    size = lt.size(lista1)
    final = float(0)
    for a in lt.iterator(lista1):
        if a["Circumference (cm)"] == None or a["Circumference (cm)"] == "":
            a["Circumference (cm)"] = 0
        if a["Depth (cm)"] == None or a["Depth (cm)"] == "":
            a["Depth (cm)"] = 0
        if a["Diameter (cm)"] == None or a["Diameter (cm)"] == "":
            a["Diameter (cm)"] = 0
        if a["Height (cm)"] == None or a["Height (cm)"] == "":
            a["Height (cm)"] = 0
        if a["Length (cm)"] == None or a["Length (cm)"] == "":
            a["Length (cm)"] = 0
        if a["Weight (kg)"] == None or a["Weight (kg)"] == "":
            a["Weight (kg)"] = 0
        if a["Width (cm)"] == None or a["Width (cm)"] == "":
            a["Width (cm)"] = 0
        kl = float(0)
        costor = float(0)
        costovolu = float(0)
        defe = 48.00
        maximo = float(0)
        mul = 72.00
        if a["Weight (kg)"] != 0:
            k = mul * float(a["Weight (kg)"])
        if a["Diameter (cm)"] != 0:
            if a["Height (cm)"] == 0: 
                r = ((float(a["Diameter (cm)"]) * (1/100))/2)
                ar = (r*r)*3.1416
                costor = mul * ar
            else: 
                r = ((float(a["Diameter (cm)"]) * (1/100))/2)
                volu = (r*r)*float(a["Height (cm)"])*3.1416
                costovolu = volu * mul
        if a["Height (cm)"] != 0  or a["Length (cm)"] != 0:
            if a["Length (cm)"] != 0:
                largo = float(a["Length (cm)"]) * (1/100)
                if a["Width (cm)"] != 0 :
                    ancho = float(a["Width (cm)"]) * (1/100)
                    area= largo*ancho
                    if a["Depth (cm)"] != 0:
                        profundo = float(a["Depth (cm)"]) * (1/100)
                        volu = area*profundo
                        costovolu = volu * mul
                    if costovolu == 0:
                        costor = area*mul
            if a["Height (cm)"] != 0:
                largo = float(a["Height (cm)"]) * (1/100)
                if a["Width (cm)"] != 0 :
                    ancho = float(a["Width (cm)"]) * (1/100)
                    area= largo*ancho
                    if a["Depth (cm)"] != 0:
                        profundo = float(a["Depth (cm)"]) * (1/100)
                        volu = area*profundo
                        costovolu = volu * mul
                    if costovolu == 0:
                        costor = area*mul
        maximo = max(costovolu,costor,kl)
        if costor == 0 and costovolu == 0 and kl ==0:
            maximo = defe
        a["Costo"] = maximo
        final += maximo
    a1 = ms.sort(lista1, sort_mas_caros)
    a1 = lt.subList(a1,1,5)
    a2 = ms.sort(lista1, sort_mas_bajos)
    a2 = lt.subList(a2,1,5)
    ffinal = (size,final,a1,a2)
    return ffinal
def sort_mas_caros(element1, element2):
    return element1["Costo"] > element2["Costo"]
def sort_mas_bajos(element1,element2):
    if element1["Date"] == "" or element1["Date"] == None:
        element1["Date"]= "9999"
    if element2["Date"] == "" or element2["Date"] == None:
        element2["Date"] = "9999" 
    return element1["Date"] < element2["Date"]
#fin req 5
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




    
        