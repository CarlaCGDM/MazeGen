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
import bpy
from bpy.types import (Panel,Operator)
from random import randint
from pathlib import Path
generador = bpy.data.texts["dibujador_laberintos.py"].as_module()

#Creamos la clase botón:
class GenerateButtonOperator(bpy.types.Operator):
    """Genera un laberinto de dimensiones semi-aleatorias con el algoritmo de PRIM."""
    bl_idname = "random.1"
    bl_label = "Generar Laberinto"

    def execute(self, context):
        generador.generar_laberinto()
        laberinto = generador.cargar_laberinto(__file__)
        generador.dibujar_laberinto(laberinto)
        camino = generador.resolver_laberinto(laberinto)
        generador.animar_resolucion_laberinto(camino)
        return {'FINISHED'}
    
#Creamos la clase menú:        
class CustomPanel(bpy.types.Panel):
    bl_label = "MazeGen Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MazeGen"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        column = layout.column()
        column.operator(GenerateButtonOperator.bl_idname, text="Generar Laberinto", icon='WORLD_DATA')


from bpy.utils import register_class, unregister_class
_classes = [
    GenerateButtonOperator,
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
