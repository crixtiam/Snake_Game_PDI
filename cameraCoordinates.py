import cv2 as cv

class cameraCoordinates:
    xanterior = 0
    yanterior = 0
    x = 0
    y = 0
    rectanglePercentage = 0.10
    colorMask = 0
    font=cv.FONT_HERSHEY_SIMPLEX

    def __init__(self):
        self.x = 0   # instance variable unique to each instance
        self.y = 0
        self.xanterior = 0
        self.yanterior = 0
        self.colorMask = 0
        self.font = cv.FONT_HERSHEY_SIMPLEX

    def dibujar(self,mask, frame):
      contour,_ = cv.findContours(mask, cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS)
      for cnt in contour:
        area = cv.contourArea(cnt)
        if area > 3000:
          M = cv.moments(cnt)
          if (M["m00"]==0): M["m00"]=1
          cx = int(M["m10"]/M["m00"])
          cy = int(M['m01']/M['m00'])

          self.x = cx
          self.y = cy

          nuevoContorno = cv.convexHull(cnt)
          x, y, h, w = cv.boundingRect(nuevoContorno)

          cv.rectangle(frame, (x,y),
                       (x + w, y + h), (255, 0, 0), 3)  # top point x+w and bottom point y+h

          #cv.rectangle(frame,x,y,(0,255,0))

          cv.circle(frame,(cx,cy),7,(0,0,255),-1)
          cv.putText(frame,'{},{}'.format(cx,cy),(cx+10,cy), self.font, 0.75,(0,255,0),1,cv.LINE_AA)
          cv.drawContours(frame, [nuevoContorno], 0, self.colorMask, 3)

    def diferenciaCoordenada(self,cx,cy):
        dx = self.x - cx
        dy = self.y  - cy
        return [dx,dy]
