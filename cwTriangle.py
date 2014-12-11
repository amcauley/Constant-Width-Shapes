import turtle
import random
import math

PARAM_SCR_SEED              = None
PARAM_FORCE_EQ              = 0
PARAM_TRIANGLE_RANGE        = 100
PARAM_BUFFER_SIZE           = 15
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

sc.setup(PARAM_TRIANGLE_RANGE*5,PARAM_TRIANGLE_RANGE*5)

def turtleReset(x,y):
    print("Turtle Reset "+str((x,y)))
    t0.reset()
    t0.hideturtle()
    t0.speed('fastest')
    t0.pensize(PARAM_PENSIZE)
    ''' python doc section 24.5.4.3 shows onclick as a mdethod of the turtle class, but it actually belongs to the screen class.
        similar issue with setup    '''
    sc.onclick(turtleReset)
    cwTriangle()

def tPendown(t):
    if (t == t0):
        t.pendown()
                
    
def cwTriangle():

    global t
    t = t0

    global cancelDrawing
    cancelDrawing = 0
    
    if(PARAM_SCR_SEED != None):
        random.seed(PARAM_SCR_SEED)
    
    a = [random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE),random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE)]
    
    b = [random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE),random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE)]
    while (b == a):
        b = [random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE),random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE)]
        
    c = [random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE),random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE)]
    while ((c == a) or (c == b)):
        c = [random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE),random.randint(-PARAM_TRIANGLE_RANGE,PARAM_TRIANGLE_RANGE)]
    
    if(PARAM_FORCE_EQ):
        a = [0,0]
        b = [PARAM_TRIANGLE_RANGE/2,PARAM_TRIANGLE_RANGE*math.sqrt(3)/2]
        c = [PARAM_TRIANGLE_RANGE,0]
    
    A = math.sqrt(pow(b[0]-c[0],2)+pow(b[1]-c[1],2))
    B = math.sqrt(pow(a[0]-c[0],2)+pow(a[1]-c[1],2))
    C = math.sqrt(pow(b[0]-a[0],2)+pow(b[1]-a[1],2))
    
    lengths = [A,B,C]
    D = min(lengths)
    lengths.remove(D)
    D = lengths[0] + lengths[1] - D + PARAM_BUFFER_SIZE
    
    AA = .5*(D+A-B-C)
    BB = .5*(D+B-A-C)
    CC = .5*(D+C-A-B)
    
    '''from documentation, circle center is radius units to the left of turtle'''

    colors = ["red","green","blue"]
    
    t.setheading(0)
    
    t.penup()
    
    if(cancelDrawing):
        return
    
    t.setpos(a[0],a[1])
    t.dot(PARAM_DOT_SIZE, colors[0])
    tPendown(t)
    hh = t.towards(b[0],b[1])
    t.setheading(hh)

    if(cancelDrawing):
        return
        
    t.setpos(b[0],b[1])
    t.dot(PARAM_DOT_SIZE, colors[1])
    abh = t.heading()
    bah = (abh+180)%360
    hh = t.towards(c[0],c[1])
    t.setheading(hh)    

    if(cancelDrawing):
        return

    t.setpos(c[0],c[1])
    t.dot(PARAM_DOT_SIZE, colors[2])
    bch = t.heading()
    cbh = (bch+180)%360
    hh = t.towards(a[0],a[1])
    t.setheading(hh)    

    if(cancelDrawing):
        return
    
    t.setpos(a[0],a[1])
    cah = t.heading()
    ach = (cah+180)%360
    t.penup()
    
    if(cancelDrawing):
        return
    
    print("abh "+str(abh)+" bah "+str(bah)+" bch "+str(bch)+
          " cbh "+str(cbh)+" cah "+str(cah)+" ach "+str(ach))
    
    ha = (abh+ach)/2
    if(math.fabs(abh-ach) >= 180):
        ha = (ha+180)%360
    hb = (bah+bch)/2
    if(math.fabs(bah-bch) >= 180):
        hb = (hb+180)%360
    hc = (cah+cbh)/2
    if(math.fabs(cah-cbh) >= 180):
        hc = (hc+180)%360
    
    ''' store lengths of opposite vertex radius with x,y locations '''
    a.extend([A,AA,ha])
    b.extend([B,BB,hb])
    c.extend([C,CC,hc])
    vertices = [a,b,c]

    print("vertices: "+str(vertices))
    
    for vidx in range(0,len(vertices)):
    
        v0 = vertices[vidx] #current vertex
        v1 = vertices[(vidx+1)%3]
        v2 = vertices[(vidx-1)%3]
        
        if(cancelDrawing):
            return
            
        t.color(colors[vidx])

        ''' find angle (in rad) of main arc using law of cosines '''
        theta = math.acos((pow(v1[-3],2)+pow(v2[-3],2)-pow(v0[-3],2))/(2*v1[-3]*v2[-3]))
        theta = theta*180/3.14159265

        if(cancelDrawing):
            return
        
        ''' draw minor arc behind the current vertex's angle '''
        r = v0[-2]
        h = (v0[-1]+180)%360
        t.setpos(v0[0],v0[1])
        t.setheading(h)
        t.forward(r)
        t.left(90)
        p = t.position()
        h = t.heading()
        tPendown(t)
        t.circle(r,-theta/2,PARAM_SPECIFY_CIRCLE_PTS)
        t.penup()
        t.setpos(p)
        tPendown(t)
        t.setheading(h)
        
        if(cancelDrawing):
            return
        
        t.circle(r,theta/2,PARAM_SPECIFY_CIRCLE_PTS)
        t.penup()

        if(cancelDrawing):
            return
        
        ''' draw major arc faced by this vertex's angle '''
        r = D - r
        h = v0[-1]
        t.setpos(v0[0],v0[1])
        t.setheading(h)
        t.forward(r)
        t.left(90)
        p = t.position()
        h = t.heading()
        tPendown(t)
        t.circle(r,-theta/2,PARAM_SPECIFY_CIRCLE_PTS)
        t.penup()
        t.setpos(p)
        tPendown(t)
        t.setheading(h)
        
        if(cancelDrawing):
            return
        
        t.circle(r,theta/2,PARAM_SPECIFY_CIRCLE_PTS)
        t.penup()
        
    ''' any routines that were going on before this one should be killed '''
    cancelDrawing = 1
    t = t1
        
    
if __name__ == "__main__":
    turtleReset(0,0)
    sc.mainloop()