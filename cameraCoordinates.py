
'''
--------------------------------------------------------------------------------
-----Clase que controla las coordenadas,dibuja los contornos  y ----------------
----------------- calcula los centroides ---------------------------------------
--------------------------------------------------------------------------------
'''

import cv2 as cv

class cameraCoordinates:   #se crea la clase llamada cameraCoordinates
    xanterior = 0           #Inicializacion de la variable publica
    yanterior = 0           #Inicializacion de la variable publica
    x = 0                   #Inicializacion de la variable publica
    y = 0                   #Inicializacion de la variable publica
    colorMask = 0           #Inicializacion de la variable publica
    font=cv.FONT_HERSHEY_SIMPLEX   #Inicializacion de la variable publica

    def __init__(self):  # Se inicializa las variables en el constructor
        self.x = 0   #se inicializa la coordenada x con cero
        self.y = 0   #se inicializa la coordenada y con cero
        self.xanterior = 0 #se inicializa la coordenada x anterior con cero
        self.yanterior = 0 #se inicializa la coordenada x anterior con cero
        self.colorMask = 0 #se inicializa la mascara vacia
        self.font = cv.FONT_HERSHEY_SIMPLEX  # se inicializa el tipo de fuente

    '''
    --------------------------------------------------------------------------------
    -----definicion del metodo dibujar que calcula el centroide y  ----------------
    ----------------- dibuja el contorno --- ---------------------------------------
    --------------------------------------------------------------------------------
    '''

    def dibujar(self,mask, frame):
      contour,_ = cv.findContours(mask, cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS)   #Encuentra el contorno de la mascara ingresada
      for cnt in contour:   #recorre el contorno punto a punto
        area = cv.contourArea(cnt)   #se calcula el area del contorno
        if area > 3000:              # se condicion que si es un area mayor a 3000px
          M = cv.moments(cnt)         #se encuentra los momentos del contorno
          if (M["m00"]==0): M["m00"]=1   #se condiciona para evitar inconsistencias matematicas indefinidas
          cx = int(M["m10"]/M["m00"])    #se calcula el centroide en x
          cy = int(M['m01']/M['m00'])    #se calcula el centroide en y

          self.x = cx                   #se ingresa como nueva coordenada central x, la hallada por el centroide x
          self.y = cy                   #se ingresa como nueva coordenada central y, la hallada por el centroide y

          nuevoContorno = cv.convexHull(cnt)    #se suaviza el contorno
          x, y, h, w = cv.boundingRect(nuevoContorno)   #se encuentran  encuentran las coordenadas rectangulares que encierran el contorno
          #se dibuja el rectangulo vacio (marco del rectangulo)
          cv.rectangle(frame, (x,y),
                       (x + w, y + h), (255, 0, 0), 3)  # punto mas alto x+w y punto mas bajo y+h


          cv.circle(frame,(cx,cy),7,(0,0,255),-1)           # Se dibuja el punto que representa el centroide (coordenada x,y)
          cv.putText(frame,'{},{}'.format(cx,cy),(cx+10,cy), self.font, 0.75,(0,255,0),1,cv.LINE_AA)  #coloca el texto de las coordenadas encontradas para mostrarlas en el display
          cv.drawContours(frame, [nuevoContorno], 0, self.colorMask, 3)  #dibuja el contorno de color rojo


    '''
    ------------------------------------------------------------------------------------------------
    -------------Funcion que permite hallar la diferencia entre coordenadas-------------------------
    ------------------------------------------------------------------------------------------------
    '''
    def diferenciaCoordenada(self,cx,cy):
        dx = self.x - cx     #se realiza la resta entre la coordenada anterior y la actual en x
        dy = self.y  - cy    #se realiza la resta entre la coordenada anterior y la actual en y
        return [dx,dy]       #retorna la diferencia
