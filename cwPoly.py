import turtle
import random
import numpy
import math
from turtleAux import *

PARAM_POLY_N                = 7
PARAM_PTS_OVERRIDE          = 1
PARAM_BUFFER_SIZE           = 0
PARAM_OVERRIDE_LEN          = 150
PARAM_CANVAS_SIZE           = 500
PARAM_DOT_SIZE              = 5
PARAM_PENSIZE               = 2
PARAM_HIDE_POLY             = 1
PARAM_HIDE_TURTLE           = 1

sc = turtle.Screen()
t  = turtle.Turtle()
xyEntry = (0,0)
entryCnt = 0

sc.setup(PARAM_CANVAS_SIZE, PARAM_CANVAS_SIZE)

def turtleReset(x,y):
    print("Turtle Reset "+str((x,y)))
    t.reset()
    if(PARAM_HIDE_TURTLE):
        t.hideturtle()
    t.speed('fastest')
    t.pensize(PARAM_PENSIZE)
    sc.onclick(turtleReset)
    cwPoly()
                

def enterPoint(x,y):
    global entryCnt
    global xyEntry
    xyEntry = (x,y)
    entryCnt = entryCnt + 1
   
   
def genUserPoly(N, t):
    ''' Generate (from user input) an N-gon. N must by an odd number (at least for now) greater than
        or equal to 3. 
        
        INPUT:  N = number of sides
                t = active turtle
        OUTPUT: <list of (x,y) vertices> '''
    
    global entryCnt
    global xyEntry
    
    sc.onclick(enterPoint)
    
    print("Creating new "+str(N)+"-gon")
    assert ((N > 2) and (N%2 == 1))
        
    ptsList = []    
        
    for v in range(N):
        oldEntryCnt = entryCnt
        input("Enter point "+str(v)+" then hit <Enter>...")
        newPt = xyEntry        
        ptsList.append(xyEntry)
        print("Point "+str(xyEntry)+" added")
        t.penup()
        t.setpos(xyEntry)
        t.dot(PARAM_DOT_SIZE)
        
        
    '''restore drawing interruption/reset callback'''    
    sc.onclick(turtleReset)
    
    return ptsList    
                
def cwPoly():
    
    if (PARAM_PTS_OVERRIDE):
        rads = 0
        radDiff = 6.28318530718/PARAM_POLY_N
        currX = -PARAM_OVERRIDE_LEN*.5
        currY = -PARAM_OVERRIDE_LEN
        pts = [(currX, currY)]
        for j in range(PARAM_POLY_N-1):
            xd = PARAM_OVERRIDE_LEN*math.cos(rads)
            yd = PARAM_OVERRIDE_LEN*math.sin(rads)
            rads = rads + radDiff
            currX = currX + xd
            currY = currY + yd
            pts.append((currX, currY))
        ''' Reverse points, since rest of code assumes they're in clockwise order. ''' 
        pts = pts[::-1]
    else:    
        pts = genUserPoly(PARAM_POLY_N, t)
    print("Polygon pts: "+str(pts))
    
    dList = []  #distance from vertex to it's sister vertex (the ccw one of the two possible choices)
    jStr = ''   #string that will be used to form the J matrix
    for k in range(PARAM_POLY_N):
        s = (k + int((PARAM_POLY_N-1)/2))%PARAM_POLY_N       
        kx = pts[k][0]
        ky = pts[k][1]
        sx = pts[s][0]
        sy = pts[s][1]
        dList.append(((kx-sx)**2+(ky-sy)**2)**.5)
    
        jRowStr = ''
        for kk in range(PARAM_POLY_N):
            if kk == s:
                jRowStr = jRowStr + '1 '  
            else:
                jRowStr = jRowStr + '0 '
        
        jStr = jStr + jRowStr + ';'
    
    print("dList: "+str(dList))
    jStr = jStr[:-1]    #get rid of final trailing ';'
    #print("jStr = "+jStr)
    J = numpy.matrix(jStr)
    print("J = "+str(J))
    
    ''' form the identity matrix '''
    I = numpy.matrix(numpy.identity(PARAM_POLY_N))
    
    ''' determine diameter '''
    D = max(dList)+PARAM_BUFFER_SIZE
    print("Diameter: "+str(D))
    
    ''' D2 holds the N x 1 diameter matrix minus the distances between vertex pairs '''
    D2 = ((numpy.matrix('1 '*PARAM_POLY_N) * D) - numpy.matrix(dList)).T
    print("D2 = "+str(D2))
   
    ''' determine the radii attached to each vertex. Note: to get element i, use R.item(i). Matrix
        elements can also be accessed as M.item(i,j). '''
    R = numpy.linalg.inv(J+I)*D2
    print("R = "+str(R))
   
    ''' Main drawing routine to go here. Will be helpful to define turtle helper functions such as drawing
       line segment from (a,b) to (c,d) and drawing an arc of radius r with center at (x,y), from angle theta
       to angle phi. '''
    for k in range(PARAM_POLY_N):
        ''' Connecting line to next vertex. '''
        if not PARAM_HIDE_POLY:
            t.color("black")
            drawLine(pts[k], pts[(k+1)%PARAM_POLY_N], t)
        ''' Small arc for this vertex. '''
        s = (k + int((PARAM_POLY_N-1)/2))%PARAM_POLY_N 
        t.color("red")
        print(str(k)+". Small arc: (center, rad, xy1, xy2) = "+str((pts[k], R.item(k), pts[s], pts[(s+1)%PARAM_POLY_N])))
        drawArc(pts[k], R.item(k), pts[s], pts[(s+1)%PARAM_POLY_N], 1, t)
        ''' Large arc for this vertex. '''
        t.color("blue")
        print(str(k)+". Large arc: (center, rad, xy1, xy2) = "+str((pts[k], R.item(k), pts[s], pts[(s+1)%PARAM_POLY_N])))
        drawArc(pts[k], D - R.item(k), pts[s], pts[(s+1)%PARAM_POLY_N], 0, t)
        
    
if __name__ == "__main__":
    turtleReset(0,0)
    sc.mainloop()