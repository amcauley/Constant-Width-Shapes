import turtle
import random
import math

def cwTriangle():

    PARAM_SCR_SEED = None
    PARAM_FORCE_EQ = 1
    PARAM_TRIANGLE_RANGE = 200
    PARAM_BUFFER_SIZE = 30
    PARAM_DOT_SIZE = 10
    
    if(PARAM_SCR_SEED != None):
        random.seed(PARAM_SCR_SEED)
    
    sc = turtle.Screen()
    t = turtle.Turtle()
    
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
    
    AA = int(.5*(D+A-B-C))
    BB = int(.5*(D+B-A-C))
    CC = int(.5*(D+C-A-B))
    
    '''from documentation, circle center is radius units to the left of turtle'''

    colors = ["red","green","blue"]
    
    t.setheading(0)
    
    t.penup()
    t.setpos(a[0],a[1])
    t.dot(PARAM_DOT_SIZE, colors[0])
    t.pendown()
    hh = t.towards(b[0],b[1])
    t.setheading(hh)
    t.setpos(b[0],b[1])
    t.dot(PARAM_DOT_SIZE, colors[1])
    abh = t.heading()
    bah = (abh+180)%360
    hh = t.towards(c[0],c[1])
    t.setheading(hh)    
    t.setpos(c[0],c[1])
    t.dot(PARAM_DOT_SIZE, colors[2])
    bch = t.heading()
    cbh = (bch+180)%360
    hh = t.towards(a[0],a[1])
    t.setheading(hh)    
    t.setpos(a[0],a[1])
    cah = t.heading()
    ach = (cah+180)%360
    t.penup()
    
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
        t.color(colors[vidx])
        ''' find angle (in rad) of main arc using law of cosines '''
        theta = math.acos((pow(v1[-3],2)+pow(v2[-3],2)-pow(v0[-3],2))/(2*v1[-3]*v2[-3]))
        theta = theta*180/3.14159
        r = v0[-2]
        h = v0[-1]
        t.setpos(v0[0],v0[1])
        t.setheading((h+180)%360)
        t.forward(r)
        t.left(90)
        t.pendown()
        t.circle(r,-theta/2)
        t.circle(r,theta)
        t.penup()
        r = D - r
        t.setpos(v0[0],v0[1])
        t.setheading(h)
        t.forward(r)
        t.left(90)
        t.pendown()
        t.circle(r,-theta/2)
        t.circle(r,theta)
        t.penup()
    
    sc.mainloop()

if __name__ == "__main__":
    cwTriangle()