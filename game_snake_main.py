'''
--------------------------------------------------------------------------
--1. Importacion de Librerias---------------------------------------------
--------------------------------------------------------------------------
'''

import cv2 as cv
import numpy as np
from cameraCoordinates import cameraCoordinates
import random, pygame, sys
from pygame.locals import *


'''
--------------------------------------------------------------------------
--2. Inicializacion de Variables------------------------------------------
--------------------------------------------------------------------------
'''


FPS = 7                                         #Inicializacion de la velocidad del Juego(fotogramas por segundo)
WINDOWWIDTH = 640                               #Ancho de la pantalla del juego
WINDOWHEIGHT = 400                              #Inicializacion del alto de la pantalla de juego
CELLSIZE = 20                                   #Tamano de cada celda de la grilla.
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)         #Cantidad de cuadros de la grilla a lo ancho
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)       #Cantidad de cuadros de la grilla a lo alto

#Definicion global de los colores utilizados para el juego en formato RGB
#Donde cada color primario varia de 0 a 255
#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR_BEGIN = BLACK
BGCOLOR = (132,103,97)
LIGHTBLUE = (193,195,224)
LIGHTYELLOW = (228,228,148)
YELLOW = (255,193,0)

#Definicion de las direcciones  de movimiento de la culebrita
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # Index de la cabeza del gusano.
#Definicion de la gama de colores en HSV para la mascara
azulBajo = np.array([100, 80, 20], np.uint8)      #Azul Claro
azulAlto = np.array([130, 255, 255], np.uint8)    #Azul Oscuro

'''
--------------------------------------------------------------------------
--3. Inicializacion del sistema-------------------------------------------
--------------------------------------------------------------------------
'''

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT         #Definicion de variables globales para el manejo del display

    pygame.init()                                   #Inicializacion de la libreria pygame
    FPSCLOCK = pygame.time.Clock()                  #metodo que permite obtener los frames por segundo del display
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))      #inicializacion del display, Tamanos
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)    #Tipo de letra y tamano
    pygame.display.set_caption('Snake')                #Titulo de la ventana del juego

    showStartScreen()       #Funcion el mensaje de bienvenida del juego
    while True:
        runGame()           #Funcion que permite generar el comportamiento del juego.
        showGameOverScreen()  #Funcion que despliega el mensaje de juego terminado y el score final

'''
--------------------------------------------------------------------------
--4. Definicion de Funciones,Metodos--------------------------------------
--------------------------------------------------------------------------
'''
def runGame():
    # Inicializacion de puntos aleatorios
    startx = random.randint(5, CELLWIDTH - 6)     # Inicializacion de un punto de inico aleatorio en x
    starty = random.randint(5, CELLHEIGHT - 6)    # Inicializacion de un punto de inico aleatorio en y
    wormCoords = [{'x': startx, 'y': starty},     # Inicializacion del cuerpo del culebrita. se utiliza un diccionario,
                  {'x': startx - 1, 'y': starty}, # para definir la parte inicial y final del cuerpo
                  {'x': startx - 2, 'y': starty}] # En este caso se crean 3 segmentos como cuerpo inicial de la culebrita
    direction = RIGHT    #Se define como direccion inicial la direccion derecha

    apple = getRandomLocation()      # Funcion que devuelve la posicion aleatoria de la manzana
    capture = cv.VideoCapture(0)     #Metodo de open cv2 que permite la inicializacion del video por medio de la camara del computador

    camera = cameraCoordinates()     #inicializacion de la clase camaraCoordinates
    camera.colorMask = (0, 0, 255)   #Definir el color del contorno de color rojo
    camera.font = cv.FONT_HERSHEY_SIMPLEX   #Definicion del tipo de letra para las coordenadas del centroide
    # coordenadas

    obstacle = getRandomLocation()


    while True:  # main game loop
        ret, frame = capture.read()     #Captur.read() retorna si el marco/frame  fue leido correctamente con un true o falsey ademas retorna el marco/frame del video
        frame = frame[0:320, 0:600]     #Para evitar un marco grande se redefine el tamano a visualizar
        if ret == True:                 # Si el marco es leido correctamente ejecuta el while
            frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  #se convierte el marco/frame  leido de video de RGB a  un frame HSV
            blueMask = cv.inRange(frameHSV, azulBajo, azulAlto)   #Metodo que deuelve una mascara en blanco y negro dependiendo del rango de color HSV a detectar.
            _, blueMask = cv.threshold(blueMask, 100, 200, cv.THRESH_BINARY)
            camera.xanterior = camera.x    #inicilizacion de la variable xanterior de la clase, esto para poder realizar la resta de pixeles
            camera.yanterior = camera.y    #inicilizacion de la variable yanterior de la clase, esto para poder realizar la resta de pixeles

            print("*************************************")

            print(f"coordenada anterior {camera.xanterior},{camera.yanterior}") #Impresion de las coordenadas
            # cada vez que pasa por la funcion dibujar el momento x,y se cambia
            camera.dibujar(blueMask, frame)      #Funcion que permite calculare el centroide y dibujar el contorno
            # El metodo permite sacar la diferencia
            dxy = camera.diferenciaCoordenada(camera.xanterior, camera.yanterior) # Metodo que permite calcular la diferencia de coordenadas mediante una resta
            print("*************************************")

            cv.imshow("Frame", frame)                       #visualizacion del marco rgb del video
            cv.imshow("FrameHSV", frameHSV[0:320,0:600])    #visualizacion del marco en HSV
            cv.imshow("MaskBlue", blueMask)                 #Visualizacion de la mascara
            key = cv.waitKey(1)
            if key == 27:
                break

        #MOVIMIENTOS EN x IZQUIERDA - DERECHA
        if (dxy[0] > 10 and dxy[0] > abs(dxy[1]) and direction != RIGHT):   #compara si dx -> diferencia en x de pixeles es superior a 10 y si es mayor al absoluto de y
            direction = LEFT                                                #con esto se asegura que hubo un movimiento significativo en x y no en Y
        elif (dxy[0] < -10 and abs(dxy[0]) > abs(dxy[1]) and direction != LEFT):  #compara si dx -> diferencia en x de pixeles es inferior a 10 y si es mayor al absoluto de y
            direction = RIGHT
        #MOVIMIENTOS EN Y ... ARRIBA Y ABAJO
        elif (dxy[1] < -10 and abs(dxy[1]) > abs(dxy[0]) and direction != DOWN): #compara si dY -> diferencia en y de pixeles es superior a 10 y si es mayor al absoluto de x
            direction = UP

        elif (dxy[1] > 10 and dxy[1] > abs(dxy[0]) and direction != UP):     #compara si dY -> diferencia en y de pixeles es inferior a 10 y si es mayor al absoluto de x
            direction = DOWN

        # Funcionamiento de teclas
        for event in pygame.event.get():  # recorre la lista de eventos de teclas oprimidas.
            if event.type == QUIT:        # detecta si se clickeo la  x de la ventana del juego
                terminate()               #llama al metodo termnate() que termina la visualizacion y el juego
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:   # Detecta la tecla scape (ESC) y termina el juego mediante el metodo llamado
                    terminate()


        #Permite a la culebrita pasar de un extremo de la pantalla a otro
        if wormCoords[HEAD]['x'] == -1:
            wormCoords[HEAD]['x'] = CELLWIDTH - 1     #mueve los segmetos de la culebrita a la derecha cuando la culebrita toca el segmento izq
        if wormCoords[HEAD]['x'] == CELLWIDTH:
            wormCoords[HEAD]['x'] = 0           #Mueve los segmentos de la culebrita a la izquierda cuado toca el segmento derecho
        if wormCoords[HEAD]['y'] == -1:
            wormCoords[HEAD]['y'] = CELLHEIGHT - 1  #mueve los segmentos a la parte de abajo cuando la culebrita toca el extemo superior
        if wormCoords[HEAD]['y'] == CELLHEIGHT:
            wormCoords[HEAD]['y'] = 0             #Mueve los segmetos a la parte de arriba cuando la culebrita toca el segmeto inferior
        #Ciclo para verificar si la culebrita se ha mordido asi misma
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']: #verificacion si la culebrita se ha modido a si misma
                return  # game over



        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']: #Se verifica si la culebrita se ha comido una manzana
            apple = getRandomLocation()  # coloca una nueva manzana en una posicion aleatoria
        else:
            del wormCoords[-1]  # Elimina la cola del segmento


        if wormCoords[HEAD]['x'] == obstacle['x'] and wormCoords[HEAD]['y'] == obstacle['y']: #Se verifica si la culebrita se ha comido una manzana
            return
        if wormCoords[HEAD]['x'] == obstacle['x'] and wormCoords[HEAD]['y'] == obstacle['y'] + CELLSIZE*2:  # Se verifica si la culebrita se ha comido una manzana
            return
        if wormCoords[HEAD]['x'] == obstacle['x'] + CELLSIZE and wormCoords[HEAD]['y'] == obstacle['y']:  # Se verifica si la culebrita se ha comido una manzana
            return
        if wormCoords[HEAD]['x'] == obstacle['x'] and wormCoords[HEAD]['y'] == obstacle['y']+ CELLSIZE *6:  # Se verifica si la culebrita se ha comido una manzana
            return



        # mueve la culebrita agregando un segmento en la dirección en que se mueve
        if direction == UP:   #verifica si la direccion de movimiento es hacia arriba
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}   #inserta nuevo segmento
        elif direction == DOWN: #verifica si la direccion de movimiento es hacia abajo
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}    #inserta nuevo segmento
        elif direction == LEFT:  #verifica si la direccion de movimiento es hacia izquierda
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}     #inserta nuevo segmento
        elif direction == RIGHT:  #verifica si la direccion de movimiento es hacia derecha
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}    #inserta nuevo segmento
        wormCoords.insert(0, newHead) #inserta un nuevo segmento
        DISPLAYSURF.fill(BGCOLOR)     # rellena el fondo del display de un color rojo claro
        drawGrid()                    # metodo que dibuja las grillas del display
        drawWorm(wormCoords)          #metodo que dibuja el gusano con las coordenadas
        drawApple(apple)              # metodo que dibuja la manzana
        #revisar
        draw_obstacle(obstacle)
        drawScore(len(wormCoords) - 3)    #metodo que dibuja el puntaje
        pygame.display.update()           #metodo que actualiza el display con los nuevos metodos
        FPSCLOCK.tick(FPS)
    capture.release()
    cv.destroyAllWindows()

'''
-------------------------------------------------------------------------------
------------------Funcion que permite imprimir el texto------------------------
------------------"Press a key to play "               ------------------------
-------------------------------------------------------------------------------
'''
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, YELLOW)  # configuracion del texto y color
    pressKeyRect = pressKeySurf.get_rect()                              #se crea un nuevo contorno con el tamaño de la imagen y las coordenadas x, y
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)     #Coordenadas donde se colocara el texto
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)                     #se guardan las posiciones en el display
'''
--------------------------------------------------------------------------------
-----Metodo que permite obtener el evento de cerrar la ventana mediante la x----
--------------------------------------------------------------------------------
'''
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:    #se checkea si se cierra la ventana del juego
        terminate()                         #Metodo que permite terminar el juego

    keyUpEvents = pygame.event.get(KEYUP)   #se obtiene los eventos del teclado
    if len(keyUpEvents) == 0:               #si la cantidad de eventos oprimidos en las teclas es igual a cero no se hace nada
        return None
    if keyUpEvents[0].key == K_ESCAPE:     #si se oprime la tecla esp se termina el juego
        terminate()                        #metodo que termina el juego
    return keyUpEvents[0].key

#Funcion que muestra el mensaje de bienvenida
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)                  #Metodo de pygame que permite dar el tipo de letra y tamano
    titleSurf1 = titleFont.render('Snake Game', True, LIGHTYELLOW, BLACK)  #Metodo que rederiza el fondo de pantalla y la letra del nombre del juego
    titleSurf2 = titleFont.render('Snake Game', True, YELLOW)              #Metodo que renderiza la segunda palabra escogida(snake game).

    degrees1 = 0  #grados de giro de la palabra 1, inicializacion
    degrees2 = 0  #grados de giro de la palabra 2, inicializacion
    while True:
        #Display inicial del juego
        DISPLAYSURF.fill(BGCOLOR_BEGIN)           #Fondo de relleno de color negro para el inicio del juego(pantalla de bienvenida)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)  #rotacion del titulo mediante el metodo .rotate.
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():   #verifica si alguna tecla fue presionada
            pygame.event.get()  # Limpia los eventos
            return
        pygame.display.update()   #actualiza el display con los nuevos metodos
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame

'''
--------------------------------------------------------------------------------
-----Metodo que permite terminar el juego --------------------------------------
--------------------------------------------------------------------------------
'''
def terminate():
    pygame.quit()    # Desactiva el evento y la libreria
    sys.exit()       # termina el programa/evento


 #Funcion que retorna un diccionario de coordenadas x,y
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)} #Retorno de la coorrdenada x y aleatoria


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)   #Tipo de letra y tamano de la fuente
    gameSurf = gameOverFont.render('Game', True, WHITE)        #color de la palabra
    overSurf = gameOverFont.render('Over', True, WHITE)        #color de la palabra
    gameRect = gameSurf.get_rect()  #Pygame crea un nuevo contorno con el tamaño de la imagen y las coordenadas x, y
    overRect = overSurf.get_rect()  #Pygame crea un nuevo contorno con el tamaño de la imagen y las coordenadas x, y
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)    #se guardan las posiciones en el display
    DISPLAYSURF.blit(overSurf, overRect)    #se guardan las posiciones en el display
    drawPressKeyMsg()                       #metodo que imprime el texto de prsionar una tecla cualquiera
    pygame.display.update()                 #Metodo que actualiza el display y carga los metodos guardados.
    pygame.time.wait(500)                   #se define un tiempo de espera antes de iniciar el juego
    checkForKeyPress()  # borrar cualquier pulsación de tecla en la cola de eventos

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


'''
--------------------------------------------------------------------------------
-----------Metodo que permite visualizar el puntaje-----------------------------
--------------------------------------------------------------------------------
'''
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE) #Impresion del puntaje en el display
    scoreRect = scoreSurf.get_rect()                                 #se crea un nuevo contorno con el tamaño de la imagen y las coordenadas x, y
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)                      #colocar el puntaje en la parte superior derecha (coodenadas invertidas)
    DISPLAYSURF.blit(scoreSurf, scoreRect)                           #se guardan las posiciones en el display


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE   #se multiplica el valor unitario aleatorio x por el tamano de la celda
        y = coord['y'] * CELLSIZE   #se multiplica el valor unitario aleatorio y por el tamano de la celda
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)   #se dibuja el contorno de la culebrita
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)  #se rellena el contorno de cada segmento de la culebrita
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE   #se multiplica el valor unitario aleatorio x por el tamano de la celda
    y = coord['y'] * CELLSIZE   #se multiplica el valor unitario aleatorio y por el tamano de la celda
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)  #Dibuja el contorno dle cuadrado con las coordenadas
    pygame.draw.rect(DISPLAYSURF, GREEN, appleRect)      #rellena el cuadradado (manzana)

def draw_obstacle(coord):
    x = coord['x'] * CELLSIZE   #se multiplica el valor unitario aleatorio x por el tamano de la celda
    y = coord['y'] * CELLSIZE   #se multiplica el valor unitario aleatorio y por el tamano de la celda
    obstacle_rect_1 = pygame.Rect(x, y, CELLSIZE, CELLSIZE)  #Dibuja el contorno dle cuadrado con las coordenadas
    obstacle_rect_2 = pygame.Rect(x, y+CELLSIZE*2, CELLSIZE, CELLSIZE)  # Dibuja el contorno dle cuadrado con las coordenadas
    obstacle_rect_3 = pygame.Rect(x + CELLSIZE, y, CELLSIZE, CELLSIZE)  # Dibuja el contorno dle cuadrado con las coordenadas
    obstacle_rect_4 = pygame.Rect(x, y + CELLSIZE * 6, CELLSIZE,CELLSIZE)  # Dibuja el contorno dle cuadrado con las coordenadas
    pygame.draw.rect(DISPLAYSURF, YELLOW, obstacle_rect_1)
    pygame.draw.rect(DISPLAYSURF, YELLOW, obstacle_rect_2)
    pygame.draw.rect(DISPLAYSURF, YELLOW, obstacle_rect_3)
    pygame.draw.rect(DISPLAYSURF, YELLOW, obstacle_rect_4)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # Ciclo que Dibuja las lineas verticales
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT)) #Dibuja un segmento vertical de color gris oscuro
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Ciclo que Dibuja lineas Horizontales
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))  #dibuja un segmento vertical de color gris oscuro

#Se identifica el metodo main el cual es lanzado para iniciar la app
if __name__ == '__main__':
    main()                      #se llama al metodo main

'''
--------------------------------------------------------------------------
--------------------------  FIN DEL PROGRAMA -----------------------------
--------------------------------------------------------------------------
'''
