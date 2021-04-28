
'''
--------------------------------------------------------------------------
------- SNAKE GAME -------------------------------------------------------
------- Coceptos básicos de PDI-------------------------------------------
------- Por: Cristiam Loaiza    cristiam.loaiza@udea.edu.co --------------
--------------------------------------------------------------------------
------------ Robinson Jaramillo robinson.jaramillov@udea.edu.co ----------
--------------------------------------------------------------------------
-------      Estudiantes de Ingenieria Electronica  ----------------------
-------      Universidad de Antioquia, Medellin --------------------------
------- Curso Básico de Procesamiento de Imágenes y Visión Artificial-----
--------------------------------------------------------------------------
--------------------------------------------------------------------------
'''

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
#WINDOWWIDTH = 640
#WINDOWHEIGHT = 480
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
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    global cdx, cdy

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake Game')

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
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)     # Inicializacion de un punto de inico aleatorio en x
    starty = random.randint(5, CELLHEIGHT - 6)    # Inicializacion de un punto de inico aleatorio en y
    wormCoords = [{'x': startx, 'y': starty},     # Inicializacion del cuerpo del culebrita. se utiliza un diccionario,
                  {'x': startx - 1, 'y': starty}, # para definir la parte inicial y final del cuerpo
                  {'x': startx - 2, 'y': starty}] # En este caso se crean 3 segmentos como cuerpo inicial de la culebrita
    direction = RIGHT    #Se define como direccion inicial la direccion derecha

    # Start the apple in a random place.
    apple = getRandomLocation()      # Funcion que devuelve la posicion aleatoria de la manzana
    capture = cv.VideoCapture(0)     #Metodo de open cv2 que permite la inicializacion del video por medio de la camara del computador


    camera = cameraCoordinates()     #inicializacion del metodo camaraCoordinates
    camera.colorMask = (0, 0, 255)
    camera.font = cv.FONT_HERSHEY_SIMPLEX
    # coordenadas
    while True:  # main game loop
        ret, frame = capture.read()     #Captur.read() retorna si el marco/frame  fue leido correctamente con un true o falsey ademas retorna el marco/frame del video
        frame = frame[0:320, 0:600]     #Para evitar un marco grande se redefine el tamano a visualizar
        if ret == True:                 # Si el marco es leido correctamente ejecuta el while
            frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  #se convierte el marco/frame  leido de video de RGB a  un frame HSV
            blueMask = cv.inRange(frameHSV, azulBajo, azulAlto)   #Metodo que deuelve una mascara en blanco y negro dependiendo del rango de color HSV a detectar.
            _, blueMask = cv.threshold(blueMask, 100, 200, cv.THRESH_BINARY)

            # print("comenzo")
            # primera coordenada
            camera.xanterior = camera.x    #inicilizacion de la variable xanterior de la clase, esto para poder realizar la resta de pixeles
            camera.yanterior = camera.y    #inicilizacion de la variable yanterior de la clase, esto para poder realizar la resta de pixeles

            print("*************************************")

            print(f"coordenada anterior {camera.xanterior},{camera.yanterior}")
            # cada vez que pasa por la funcion dibujar el momento x,y se cambia
            camera.dibujar(blueMask, frame)
            # sacar la diferencia, valores anteriores x,y antes de ejecutar la funcion dibujar
            # valores x,y despues de ejecutar dibujar.

            dxy = camera.diferenciaCoordenada(camera.xanterior, camera.yanterior)

            # print(f"coordenada dx {dxy[0]}, coordenada dy {dxy[1]}")

            if (abs(dxy[0]) >= 50 or abs(dxy[1]) >= 50):
                print(f"coordenada posterior {camera.x},{camera.y}")
                print(f"coordenada dx {dxy[0]}, coordenada dy {dxy[1]}")

            print("*************************************")

            # print(f"coordenada x: {camera.x} coordenada y {camera.y}")
            #contours, _ = cv.findContours(blueMask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            # print("final")

            cv.imshow("Frame", frame)
            cv.imshow("FrameHSV", frameHSV[0:320,0:600])
            cv.imshow("MaskBlue", blueMask)
            key = cv.waitKey(1)
            if key == 27:
                break

        # dx = dxy[0]  dy = dxy[1]

        if (dxy[0] > 20 and dxy[0] > abs(dxy[1]) and direction != RIGHT):
            direction = LEFT
        elif (dxy[0] < -20 and abs(dxy[0]) > abs(dxy[1]) and direction != LEFT):
            direction = RIGHT
        elif (dxy[1] < -20 and abs(dxy[1]) > abs(dxy[0]) and direction != DOWN):
            direction = UP

        elif (dxy[1] > 20 and dxy[1] > abs(dxy[0]) and direction != UP):
            direction = DOWN

        # Funcionamiento de teclas
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1:
            wormCoords[HEAD]['x'] = CELLWIDTH - 1

        if wormCoords[HEAD]['x'] == CELLWIDTH:
            wormCoords[HEAD]['x'] = 0

        if wormCoords[HEAD]['y'] == -1:
            wormCoords[HEAD]['y'] = CELLHEIGHT - 1
        if wormCoords[HEAD]['y'] == CELLHEIGHT:
            wormCoords[HEAD]['y'] = 0

        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
        else:
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    capture.release()
    cv.destroyAllWindows()


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, YELLOW)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

#Funcion que muestra el mensaje de bienvenida
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)                  #Metodo de pygame que permite dar el tipo de letra y tamano
    titleSurf1 = titleFont.render('Snake Game', True, LIGHTYELLOW, BLACK)  #Metodo que rederiza el fondo de pantalla y la letra del nombre del juego
    titleSurf2 = titleFont.render('Snake Game', True, YELLOW)              #Metodo que renderiza la segunda palabra escogida(snake game).

    degrees1 = 0
    degrees2 = 0
    while True:
        #Display inicial del juego
        DISPLAYSURF.fill(BGCOLOR_BEGIN)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()

 #Funcion que retorna un diccionario de coordenadas x,y
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()

'''
--------------------------------------------------------------------------
--------------------------  FIN DEL PROGRAMA -----------------------------
--------------------------------------------------------------------------
'''
