###########################################################################################
#                                                                                         #
#                                  GENERADOR DE LABERINTOS                                #
#                                     github/CarlaCGDM                                    #
#                                                                                         #
###########################################################################################

###########################################################################################
#                                      INFO DEL ADDON                                     #
###########################################################################################

bl_info = {
    "name": "MazeGen",
    "author": "SquirrelCarla",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N",
    "description": "Genera un laberinto y una animación de su resolución.",
    "warning": "",
    "doc_url": "",
    "category": "",
}

###########################################################################################
#                                           MODULOS                                       #
###########################################################################################

import bpy
from bpy.types import (Panel,Operator)
from random import randint
from pathlib import Path

def cargar_ficheros():
    ficheros = ['script.py','generador_laberintos.py','resolvedor_laberintos.py']
    raiz = Path(__file__).parents[1]
    for fichero in ficheros:
        ruta_fichero = str(raiz) + '\\addons\\' + fichero
        print(ruta_fichero)
        try:
            print(bpy.data.texts[fichero])
        except:
            bpy.data.texts.load(ruta_fichero)
    
###########################################################################################
#                                        BOTONES                                          #
###########################################################################################

#Creamos la clase botón:
class GenerateButtonOperator(bpy.types.Operator):
    """Genera un laberinto de dimensiones semi-aleatorias con el algoritmo de PRIM."""
    bl_idname = "mazegen.generar"
    bl_label = "Generar Laberinto"

    def execute(self, context):
        cargar_ficheros()
        generador = bpy.data.texts["script.py"].as_module()
        global laberinto
        laberinto = generador.generar_laberinto()
        generador.dibujar_laberinto(laberinto)
        return {'FINISHED'}
    
#Creamos la clase botón:
class AnimateButtonOperator(bpy.types.Operator):
    """Genera una animacion que resuelve el laberinto con el algoritmo BFS."""
    bl_idname = "mazegen.animar"
    bl_label = "Generar Laberinto"

    def execute(self, context):
        generador = bpy.data.texts["script.py"].as_module()
        camino = generador.resolver_laberinto(laberinto)
        generador.animar_resolucion_laberinto(camino)
        return {'FINISHED'}
    
###########################################################################################
#                                    MENÚ PRINCIPAL                                       #
###########################################################################################
    
#Creamos la clase menú:        
class CustomPanel(bpy.types.Panel):
    bl_label = "MazeGen"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MazeGen"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        column = layout.column()
        column.operator(GenerateButtonOperator.bl_idname, text="Generar Laberinto", icon='WORLD_DATA')
        column.operator(AnimateButtonOperator.bl_idname, text="Animar Laberinto", icon='WORLD_DATA')

###########################################################################################
#                                   REGISTRAR ADDON                                       #
###########################################################################################

from bpy.utils import register_class, unregister_class
_classes = [
    GenerateButtonOperator,
    AnimateButtonOperator,
    CustomPanel
]

def register():
    for cls in _classes:
        register_class(cls)

def unregister():
    for cls in _classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()
