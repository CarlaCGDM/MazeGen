import numpy as np
import random
from collections import deque

#-------------------------------------------------------------------------------------#
#                             CONVIRTIENDO LA MATRIZ A GRAFO                          #
#-------------------------------------------------------------------------------------#

def caminos(punto:tuple, matriz:np.array):
    w,h = matriz.shape
    caminos_posibles = []
    direcciones = [
        (punto[0]-1,punto[1]), #Arriba
        (punto[0]+1,punto[1]), #Abajo
        (punto[0],punto[1]+1), #Derecha
        (punto[0],punto[1]-1) #Izquierda
    ]
    for direccion in direcciones:
        if direccion != punto and direccion[0] in range(0,w) and direccion[1] in range(0,h):
            if matriz[direccion] != 0:
                caminos_posibles.append(direccion)
    return caminos_posibles

def grafo_desde_matriz(punto:tuple,matriz:np.array,grafo={}):
    grafo[punto] = caminos(punto,matriz)
    for camino in grafo[punto]:
        if camino not in grafo:
            grafo = {**grafo, **grafo_desde_matriz(camino,matriz,grafo)}
    return grafo

#-------------------------------------------------------------------------------------#
#                                 RESOLVIENDO EL LABERINTO                            #
#                                     (Algoritmo BFS)                                 #
#-------------------------------------------------------------------------------------#

def encontrar_camino(matriz, entrada, salida):
    #En la cola guarda un punto y el camino que se ha seguido para llegar hasta él.
    grafo = grafo_desde_matriz(entrada,matriz)
    cola = [(entrada,[entrada])]
    visitados = []
    while cola:
        punto, camino = cola.pop(0)
        visitados.append(punto)
        posibles = grafo[punto]
        random.shuffle(posibles)
        for nodo in posibles:
            if nodo == salida:
                return camino + [salida]
            else:
                if visitados.count(nodo) < 1:
                    visitados.append(nodo)
                    cola.append((nodo, camino + [nodo]))