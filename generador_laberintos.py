import random

#############################################################################
#                                                                           #
#                         GENERADOR DE LABERINTOS                           #
#                            ALGORITMO DE PRIM                              #
#                                                                           #
#                 Artículo de referencia: shorturl.at/evQRT                 #
#                                                                           #
#---------------------------------------------------------------------------#
#                                                                           #
#  -Generamos un laberinto vacío.                                           #
#  -Elegimos al azar un punto que no esté en ningún borde.                  #
#  -Marcamos ese punto como camino y sus adyacentes como paredes.           #
#  -Por cada pared, vemos si detrás de ella hay una casilla vacía.          #
#  -Vemos también que no tenga ya más de un camino adyacente.               #
#  -Si es así, la convertimos en camino y a sus adyacentes en paredes.      #
#  -Repetimos esta operación hasta que no queden más paredes por evaluar.   #
#  -Dividimos los bordes en cuadrantes a,b,c,d.                             #
#  -Marcamos una casilla adyacente a un camino como entrada en uno.         #
#  -Y hacemos lo mismo para la salida en el cuadrante opuesto.              #
#  -Sustituimos cualquier casilla vacía restante por una pared.             #
#  -Y habremos terminado el laberinto.                                      #
#                                                                           #
#############################################################################

#############################################################################
#                  FUNCIÓN QUE DEVUELVE UN LABERINTO VACÍO                  #
#            (Todas las casillas están marcadas como inexploradas)          #
#############################################################################

def laberinto_vacio(ancho,alto):
    laberinto = []
    for i in range(alto):
        linea = []
        for j in range(ancho):
            linea.append('i')
        laberinto.append(linea)

    return laberinto

#############################################################################
#     FUNCIÓN QUE DEVUELVE UN PUNTO A PARTIR DEL CUAL GENERAR CAMINOS       #
#      (Se asegura de que el punto no esté en ninguno de los bordes)        #
#############################################################################

def punto_inicial(laberinto):

    alto = len(laberinto)
    ancho = len(laberinto[0])

    #Elegimos un punto inicial al azar:
    posicion_vertical = int(random.random()*alto)
    posicion_horizontal = int(random.random()*ancho)

    #Lo movemos un poco si se encuentra en alguno de los bordes:
    if posicion_vertical == 0:
     posicion_vertical += 1
    if posicion_vertical == alto-1:
     posicion_vertical -=1
    if posicion_horizontal == 0:
        posicion_horizontal += 1
    if posicion_horizontal == ancho-1:
     posicion_horizontal -= 1

    return (posicion_vertical,posicion_horizontal)

#############################################################################
#   FUNCIÓN QUE DEVUELVE LOS VALORES DE LAS CELDAS ADYACENTES A OTRA CELDA  #
#                 (Si la celda no existe, su valor es None)                 #
#############################################################################

def valores_adyacentes(laberinto,celda):
    direcciones = [[0,1],[0,-1],[1,0],[-1,0]] 
    celdas_adyacentes = []
    valores = []
    for direccion in direcciones:
        celdas_adyacentes.append((celda[0]+direccion[0],celda[1]+direccion[1]))
    for celda in celdas_adyacentes:
        y,x = celda
        try:
            valores.append(laberinto[y][x])
        except:
            valores.append(None)
    return valores

#############################################################################
#           FUNCIÓN QUE DEVUELVE LAS CELDAS ADYACENTES A OTRA CELDA         #
#                    (Sin contar los bordes del laberinto)                  #
#############################################################################

def celdas_adyacentes(laberinto,celda):
        alto = len(laberinto)
        ancho = len(laberinto[0])
        direcciones = [[0,1],[0,-1],[1,0],[-1,0]]
        paredes = []
        for direccion in direcciones:
            c_alto = celda[0]+direccion[0]
            c_ancho = celda[1]+direccion[1]
            if c_alto in range(1,alto-1) and c_ancho in range(1,ancho-1):
                paredes.append((c_alto,c_ancho))
        return paredes

#############################################################################
#       FUNCIÓN QUE CUENTA CUANTOS CAMINOS TIENE ALREDEDOR UNA CELDA        #
#---------------------------------------------------------------------------#
#   -Sirve para evitar abrir demasiados caminos adyacentes unos a otros     #
#   -Cambiar el valor del límite genera estilos distintos de laberintos     #
#############################################################################

def recuento_caminos_adyacentes(laberinto,celda):
    caminos_totales = 0
    caminos = celdas_adyacentes(laberinto,celda)
    for celda in caminos:
        if laberinto[celda[0]][celda[1]] == 'c':
            caminos_totales += 1
    return caminos_totales

#############################################################################
#FUNCIÓN QUE DEVUELVE LAS NUEVAS PAREDES QUE SE GENERAN EN TORNO A UNA CELDA#
#   (Devuelve tupla con lista de nuevos caminos y lista de nuevas paredes)  #
#############################################################################

def nuevas_paredes(laberinto,celda):
    nuevas_paredes = []
    adyacentes = celdas_adyacentes(laberinto,celda)
    for adyacente in adyacentes:
        y,x = adyacente
        if laberinto[y][x] == 'i':
            nuevas_paredes.append((y,x))
    return nuevas_paredes

#############################################################################
#                 FUNCIÓN QUE ABRE CAMINOS EN UN LABERINTO                  #
#   (Devuelve tupla con lista de nuevos caminos y lista de nuevas paredes)  #
#############################################################################

def abrir_caminos(laberinto,pared):
    caminos = []
    paredes = []
    valores = valores_adyacentes(laberinto,pared)
    #Si la pared que estamos evaluando divide un camino y una celda inexplorada
    if valores[0] == 'c' and valores[1] == 'i':
        if recuento_caminos_adyacentes(laberinto,pared) < 2:
            caminos.append(pared)
            paredes += (nuevas_paredes(laberinto,pared))

    if  valores[0] == 'i' and  valores[1] == 'c':
        if recuento_caminos_adyacentes(laberinto,pared) < 2:
            caminos.append(pared)
            paredes += (nuevas_paredes(laberinto,pared))

    if  valores[2] == 'c' and valores[3] == 'i':
        if recuento_caminos_adyacentes(laberinto,pared) < 2:
            caminos.append(pared)
            paredes += (nuevas_paredes(laberinto,pared))

    if  valores[2] == 'i' and valores[3] == 'c':
        if recuento_caminos_adyacentes(laberinto,pared) < 2:
            caminos.append(pared)
            paredes += (nuevas_paredes(laberinto,pared))
    return caminos,paredes

#############################################################################
#         FUNCIÓN QUE DIVIDE LOS BORDES DE UN LABERINTO EN CUADRANTES       #
#                (Sigue el sentido de las agujas del reloj.)                #
#############################################################################

def definir_cuadrantes(laberinto):
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    alto = len(laberinto)
    ancho = len(laberinto[0])

    #Cuadrante superior izquierdo
    for i in range(ancho//2):
        c1.append((0,i))
    for i in range(alto//2):
        c1.append((i,0))

    #Cuadrante superior derecho
    for i in range(ancho//2,ancho):
         c2.append((0,i))
    for i in range(alto//2):
         c2.append((i,ancho-1))

    #Cuadrante inferior derecho
    for i in range(ancho//2,ancho):
        c3.append((alto-1,i))
    for i in range(alto//2,alto):
        c3.append((i,ancho-1))
    
    #Cuadrante inferior izquierdo
    for i in range(ancho//2):
        c4.append((alto-1,i))
    for i in range(alto//2,alto):
        c4.append((i,0))
    
    return [c1,c3],[c2,c4]

#############################################################################
#       FUNCIÓN QUE ENCUENTRA UNA ENTRADA Y UNA SALIDA EN UN LABERINTO      #
#    (Se asegura de que la entrada y la salida no están demasiado cerca.)   #
#############################################################################

def entrada_salida(laberinto):

    #Dividimos los bordes del laberinto en cuadrantes:
    opuestos1,opuestos2 = definir_cuadrantes(laberinto)
    random.shuffle(opuestos1)
    random.shuffle(opuestos2)
    cuadrantes = random.choice([opuestos1,opuestos2])
    #Identificamos el cuadrante de entrada y el de salida:
    cuadrante_entrada = cuadrantes[0]
    cuadrante_salida = cuadrantes[1]
    
    #Elegimos una entrada:
    entrada = None
    random.shuffle(cuadrante_entrada)
    for celda in cuadrante_entrada:
        if recuento_caminos_adyacentes(laberinto,celda) > 0:
            entrada = celda
            break

    #Elegimos una salida:
    salida = None
    random.shuffle(cuadrante_salida)
    for celda in cuadrante_salida:
        if recuento_caminos_adyacentes(laberinto,celda) > 0:
            salida = celda
            break

    return entrada,salida

#############################################################################
#     FUNCIÓN QUE DEVUELVE LAS CELDAS DE UN LABERINTO CON UN VALOR DADO     #
#############################################################################
    
def encontrar_valores(laberinto,valor):
    celdas = []
    alto = len(laberinto)
    ancho = len(laberinto[0])
    for i in range(alto):
        for j in range(ancho):
            if laberinto[i][j] == valor:
                celdas.append((i,j))
    return celdas

#############################################################################
#                FUNCIÓN QUE DEVUELVE UN LABERINTO GENERADO                 #
#############################################################################

def generar_laberinto(ancho:int,alto:int):
    #Laberinto vacío:
    laberinto = laberinto_vacio(ancho,alto)
    #Punto inicial:
    inicio = punto_inicial(laberinto)
    laberinto[inicio[0]][inicio[1]] = 'c'
    #Paredes alrededor del punto inicial:
    paredes = []
    paredes += celdas_adyacentes(laberinto,inicio)
    for pared in paredes:
        laberinto[pared[0]][pared[1]] = 'p'
    #Abrir caminos a partir del punto inicial:
    while paredes:
        random.shuffle(paredes)
        pared_aleatoria = paredes[0]
        nuevos_caminos, nuevas_paredes = abrir_caminos(laberinto,pared_aleatoria)
        for camino in nuevos_caminos:
            laberinto[camino[0]][camino[1]] = 'c'
        for pared in nuevas_paredes:
            laberinto[pared[0]][pared[1]] = 'p'
            if pared not in paredes:
                paredes.append(pared)
        paredes.remove(pared_aleatoria)
    #Encontramos una entrada y una salida:
    entrada,salida = entrada_salida(laberinto)
    laberinto[entrada[0]][entrada[1]] = 'e'
    laberinto[salida[0]][salida[1]] = 's'

    #Convertimos las casillas restantes de los bordes en paredes:
    inexploradas = encontrar_valores(laberinto,'i')
    for celda in inexploradas:
        laberinto[celda[0]][celda[1]] = 'p'

    return laberinto

#############################################################################
#             FUNCIÓN QUE EXPORTA UN LABERINTO A UN FICHERO CSV             #
#            (Caminos = 1, Paredes = 0, Entrada = 2, Salida = 3)            #
#############################################################################

def exportar_laberinto(laberinto,salida='salida.csv',separador=','):
    f_salida = open(salida, 'w')
    diccionario = {'p': '0','c': '1','e': '2','s': '3'}

    alto = len(laberinto)
    ancho = len(laberinto[0])
    for i in range(alto):
        fila = laberinto[i]
        linea = ""
        for j in range(ancho):
            valor = laberinto[i][j]
            valor_convertido = diccionario[valor]
            linea += valor_convertido
            linea += separador
        f_salida.write(linea[:-1] + '\n')
    