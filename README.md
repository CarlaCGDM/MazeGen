# MazeGen
### V.1.0
Addon para Blender que permite generar laberintos y animaciones que los recorren.

![mazegen_01](https://user-images.githubusercontent.com/92323990/171994106-5b812e5e-2171-4ee9-be7f-cb91866f95e1.gif)

### Funcionamiento:
Los laberintos se generan mediante una implementación del algoritmo de Prim. Después, se resuelven con una implementación del algoritmo BFS que devuelve el camino más corto entre el punto de entrada y el punto de salida. 

En blender, se representa gráficamente la matriz haciendo uso de la librería BPY y posteriormente se genera la animación insertando un keyframe para cada punto del recorrido. 

### Instalación:
Descarga el fichero MazeGen.zip y cárgalo desde 'Edit' -> 'Preferences' -> 'Addons' -> 'Install...'. La pestaña "MazeGen" aparecerá en la barra lateral derecha de la vista 3D (N-Panel).

(añadir gif)

### Futuras funciones:
-[x] Generar laberinto y animación de manera independiente.
-[ ] Elegir materiales.
-[ ] Elegir dimensiones.
- Posibilidad de elegir entre distintos algoritmos de resolución. 
- Generar laberinto en el origen del centro de coordenadas.
- Generar automáticamente una cámara que lo enfoque correctamente.
- Posibilidad de permitir al usuario incorporar sus propios algoritmos de resolución para visualizarlos.
