import turtle
import random
import math
import numpy

PARAM_POLY_N                = 3
PARAM_SCR_SEED              = None
PARAM_FORCE_EQ              = 0
PARAM_CANVAS_SIZE           = 500
PARAM_BUFFER_SIZE           = 10
PARAM_DOT_SIZE              = 5
PARAM_SPECIFY_CIRCLE_PTS    = None
PARAM_PENSIZE               = 2

sc = turtle.Screen()
t0 = turtle.Turtle()
t1 = turtle.Turtle()
t = t0
t1.hideturtle()
t1.penup()
t1.speed('fastest')
cancelDrawing = 0
xyEntry = (0,0)
entryCnt = 0

sc.setup(PARAM_CANVAS_SIZE, PARAM_CANVAS_SIZE)

def turtleReset(x,y):
    print("Turtle Reset "+str((x,y)))
    t0.reset()
    t0.hideturtle()
    t0.speed('fastest')
    t0.pensize(PARAM_PENSIZE)
    sc.onclick(turtleReset)
    cwPoly()

def tPendown(t):
    if (t == t0):
        t.pendown()
                

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
    global t
    t = t0

    global cancelDrawing
    cancelDrawing = 0
    
    pts = genUserPoly(PARAM_POLY_N, t)
    print("Polygon pts: "+str(pts))
    
    dList = []  #distance from vertex to it's sister vertex (the ccw one of the two possible choices)
    jStr = ''   #string that will be used to form the J matrix
    for k in range(PARAM_POLY_N):
        s = (k + int((PARAM_POLY_N+1)/2))%PARAM_POLY_N       
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
   
    '''Main drawing routine to go here. Will be helpful to define turtle helper functions such as drawing
       line segment from (a,b) to (c,d) and drawing an arc of radius r with center at (x,y), from angle theta
       to angle phi. '''
    
        
    ''' Any routines that were running before this one should be killed. '''
    cancelDrawing = 1
    t = t1
        
    
if __name__ == "__main__":
    if(PARAM_SCR_SEED != None):
        random.seed(PARAM_SCR_SEED)
    turtleReset(0,0)
    sc.mainloop()