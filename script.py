#API de Blender (BPY): https://docs.blender.org/api/current/index.html

import bpy
import numpy
import random
from collections import deque  
from pathlib import Path

#Importamos nuestros propios modulos:
generador = bpy.data.texts["generador_laberintos.py"].as_module()
resolvedor = bpy.data.texts["resolvedor_laberintos.py"].as_module()

#-------------------------------------------------------------------------------------------#
#                                   GENERAR EL LABERINTO                                    #
#-------------------------------------------------------------------------------------------#

def generar_laberinto(min=10,max=15):
    #Valores semi-aleatorios del laberinto:
    alto = random.randint(min,max)
    ancho = random.randint(min,max)

    #Generamos un laberinto y lo convertimos en array de numpy:
    laberinto_generado = generador.generar_laberinto(ancho,alto)
    laberinto_formateado = generador.formatear_laberinto(laberinto_generado,0,1,2,3)
    return numpy.array(laberinto_formateado)

#-------------------------------------------------------------------------------------------#
#                                   RESOLVER EL LABERINTO                                   #
#-------------------------------------------------------------------------------------------#

def resolver_laberinto(matriz):
    #Identificamos los puntos de entrada y de salida:
    entrada = numpy.where(matriz == 2)
    entrada = (entrada[0][0],entrada[1][0])

    salida = numpy.where(matriz == 3)
    salida = (salida[0][0],salida[1][0])
    
    #Obtenemos el camino que resuelve el laberinto
    camino = resolvedor.encontrar_camino(matriz,entrada,salida)
    return camino

#-------------------------------------------------------------------------------------------#
#                                      REPRESENTAR EN 3D                                    #
#-------------------------------------------------------------------------------------------#

def dibujar_laberinto(matriz):
    #Obtenemos las dimensiones del laberinto:
    w,h = matriz.shape
    
    #Limpiamos la escena:
    #TODO: Limpiar solo los contenidos de la coleccion laberinto! 
    materiales_escena = bpy.data.materials
    for m in materiales_escena:
        materiales_escena.remove(m)
        
    for m in bpy.data.meshes:
        bpy.data.meshes.remove(m)
        
    for c in bpy.data.collections:
        bpy.data.collections.remove(c)

    #Creamos una nueva colección:
    laberinto = bpy.data.collections.new('Laberinto')
    bpy.context.scene.collection.children.link(laberinto)

    #Creamos los nuevos materiales (en un futuro los pasaremos como parámetro del addon): 
    materiales = [
        {'nombre':'M_Base','color':(0.5,0.03,0.01,1),'metalizado':0},
        {'nombre':'M_Muro','color':(1,0.116,0.06,1),'metalizado':0},
        {'nombre':'M_Pelota','color':(0,1,1,1),'metalizado':1}
    ]

    for i in range(0,len(materiales)):
        material = materiales[i]
        bpy.data.materials.new(material['nombre'])
        bpy.data.materials[material['nombre']].diffuse_color =  material['color']
        bpy.data.materials[material['nombre']].metallic = material['metalizado']

    #Creamos una coleccion para guardar los muros:
    muros = bpy.data.collections.new("Muros")
    bpy.data.collections['Laberinto'].children.link(muros)

    #Recorremos el laberinto en busca de muros y los agregamos a la colección:
    for i in range(w):
        for j in range(h):
            if matriz[i,j] == 0:
                bpy.ops.mesh.primitive_cube_add(size=1.0,location=(i+0.5,j+0.5,0.5))
                bpy.context.active_object.data.materials.append(bpy.data.materials["M_Muro"])
                bpy.context.active_object.name = "Muro"
                muros.objects.link(bpy.context.active_object)
                bpy.context.scene.collection.objects.unlink(bpy.context.active_object)

    #Añadimos una base con las dimensiones del laberinto:
    bpy.ops.mesh.primitive_cube_add(size=0.5,location=(w/2, h/2, -0.25))
    bpy.context.active_object.data.materials.append(bpy.data.materials["M_Base"])
    bpy.context.active_object.name = "Base"
    bpy.ops.transform.resize(value=(w*2, h*2, 1))

    laberinto.objects.link(bpy.context.active_object)
    bpy.context.scene.collection.objects.unlink(bpy.context.active_object)
            
#-------------------------------------------------------------------------------------------#
#                                            ANIMAR                                         #
#-------------------------------------------------------------------------------------------#

def animar_resolucion_laberinto(camino):
    #Añadimos la pelota que recorrerá el laberinto:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5)
    bpy.context.active_object.data.materials.append(bpy.data.materials["M_Pelota"])
    bpy.context.active_object.name = "Pelota"

    for p in bpy.context.active_object.data.polygons:
        p.use_smooth = True

    bpy.data.collections['Laberinto'].objects.link(bpy.context.active_object)
    bpy.context.scene.collection.objects.unlink(bpy.context.active_object)
    
    #Generamos una animación en la cual la pelota recorre el laberinto:
    duracion = len(camino)*3

    for i in range(duracion):
        if i%3 == 0:
            paso = camino[i//3]
            bpy.data.objects['Pelota'].location=(paso[0]+0.5,paso[1]+0.5,0.5)
            bpy.data.objects['Pelota'].keyframe_insert(data_path = "location", frame = i)
        
    #Ajustamos la duracion de la animación:
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = duracion
