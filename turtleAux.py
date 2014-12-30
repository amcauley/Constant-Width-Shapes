import turtle

def drawLine(xy1, xy2, t):
    ''' Draw a line from xy1 = (x1,y1) to xy2 = (x2,y2). '''
    t.penup()
    t.setpos(xy1)
    t.pendown()
    t.setpos(xy2)
    t.penup()
    
def drawArc(cxy, r, xy1, xy2, flip, t):
    ''' Center of circle is (x,y), radius r. Arc covers the segment formed
        by xy1, cxy, xy2. Arc is drawn clockwise starting from the cxy, xy1 line.
        flip determines whether or not the arc is flipped 180 degrees around cxy. '''

    t.penup()
    t.setpos(cxy)
    t.setheading(0)
    h2 = t.towards(xy2)
    h1 = t.towards(xy1)
    if(flip):
        t.setheading((h2+180)%360)
    else:
        t.setheading(h2)
    dh = h1 - h2
    if (dh < 0):
        dh = dh + 360
    else:
        dh = dh%360
    t.forward(r)
    t.left(90)
    t.pendown()    
    t.circle(r, dh)
    t.penup()
    
    
    

