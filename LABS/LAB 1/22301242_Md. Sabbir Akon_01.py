# #TASK 1

# import OpenGL
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# w,h=800,600
# drops= []
# dc=40
# bend=0.0
# day=True
# seed=1
# def my_random():
#     global seed
#     seed=(1103515245*seed+12345)&0x7FFFFFFF
#     return seed/0x7FFFFFFF

# def display():#background 
#     if day:
#         glClearColor(0.1, 0.4, 0.8, 1.0)
#     else:
#         glClearColor(0.2, 0.2, 0.2, 1.0)
    
#     glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
#     drawGround()
#     drawHouse()
#     drawRain()
    
#     glutSwapBuffers()

# def drawHouse():
#     glColor3f(0.9, 0.9, 0.9)#bodystarts
#     glBegin(GL_TRIANGLES)
#     glVertex2f(225, 150); glVertex2f(575, 150); glVertex2f(575, 325)
#     glVertex2f(575, 325); glVertex2f(225, 325); glVertex2f(225, 150)
#     glEnd()

#     #Roof
#     glColor3f(0.2, 0.2, 0.7)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(200, 325); glVertex2f(600, 325); glVertex2f(400, 425)
#     glEnd()
#     # Door
#     glColor3f(0.3, 0.3, 0.8)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(360, 150); glVertex2f(440, 150); glVertex2f(440, 250)
#     glVertex2f(440, 250); glVertex2f(360, 250); glVertex2f(360, 150)
#     glEnd()
#     glColor3f(0,0,0)
#     glPointSize(4.0)
#     glBegin(GL_POINTS)
#     glVertex2f(425, 200)
#     glEnd()
#     # Windows
#     glColor3f(0.6, 0.6, 1.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(250, 220); glVertex2f(330, 220); glVertex2f(330, 280)
#     glVertex2f(330, 280); glVertex2f(250, 280); glVertex2f(250, 220)
#     glEnd()
#     glBegin(GL_TRIANGLES)
#     glVertex2f(470, 220); glVertex2f(550, 220); glVertex2f(550, 280)
#     glVertex2f(550, 280); glVertex2f(470, 280); glVertex2f(470, 220)
#     glEnd()
#     #Wp
#     glColor3f(0,0,0)
#     glLineWidth(2.0)
#     glBegin(GL_LINES)
#     glVertex2f(290, 220); glVertex2f(290, 280)
#     glVertex2f(250, 250); glVertex2f(330, 250)
#     glVertex2f(510, 220); glVertex2f(510, 280)
#     glVertex2f(470, 250); glVertex2f(550, 250)
#     glEnd()

# def keyboard(key, x, y):
#     global day
#     decoded_key=key.decode("utf-8").lower()
#     if decoded_key=='w':
#         day=True
#     elif decoded_key=='s':
#         day=False
#     elif key == b'\x1b':
#         glutLeaveMainLoop()

# def make_rain():
#     global drops
#     for i in range(dc):
#         x=0+my_random()*(w -0)
#         y=h+ my_random()*(h*1.5-h)
#         drop ={
#             'x1':x,'y1':y,
#             'x2':x,'y2':y+20,
#             'speed':4+my_random()*(7-4)
#         }
#         drops.append(drop)

# def drawGround():
#     #Ground
#     glColor3f(0.5, 0.3, 0.1)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(0, 0);glVertex2f(w,0);glVertex2f(w,h/3)
#     glVertex2f(w,h/3); glVertex2f(0,h/3); glVertex2f(0, 0)
#     glEnd()
#     #Trees
#     glColor3f(0.1, 0.4, 0.1)
#     for x in range(0,w, 40):
#         glBegin(GL_TRIANGLES)
#         glVertex2f(x, h/3)
#         glVertex2f(x+30,h/3+50)
#         glVertex2f(x+50,h/ 3)
#         glEnd()

# def animation():
#     global drops
#     for drop in drops:
#         drop['y1']-=drop['speed']
#         drop['y2']-=drop['speed']
#         drop['x1']+=bend
#         drop['x2']+=bend
        
#         #reset rain
#         if drop['y2'] < 0:
#             x=0+my_random()*(w -0)
#             y=h+(0+ my_random()*(100 -0))
#             drop['y1']=y
#             drop['y2']=y +20
#             drop['x1']=x
#             drop['x2']=x
        
#         if drop['x2']<0:
#             drop['x1']+=w
#             drop['x2']+=w
#         elif drop['x1']> w:
#             drop['x1']-=w
#             drop['x2']-= w
#     glutPostRedisplay()

# def drawRain():
#     glColor3f(0.7, 0.7, 1.0)
#     glLineWidth(1.5)
#     glBegin(GL_LINES)
#     for drop in drops:
#         glVertex2f(drop['x1'], drop['y1'])
#         glVertex2f(drop['x2'], drop['y2'])
#     glEnd()

# def bKeys(key,x,y):
#     global bend
#     if key==GLUT_KEY_LEFT:
#         bend=max(-5.0, bend-0.1)
#     elif key==GLUT_KEY_RIGHT:
#         bend=min(5.0,bend+0.1)

# def init():
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0,w,0.0,h,-1.0,1.0)

# glutInit([])
# glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
# glutInitWindowSize(w, h)
# glutInitWindowPosition(100, 100)
# wind = glutCreateWindow(b"Task 1")
# init()
# print("Controls:Arrows, w(Day), s(Night), ESC(Exit)")
# make_rain()

# glutDisplayFunc(display)
# glutIdleFunc(animation)
# glutKeyboardFunc(keyboard)
# glutSpecialFunc(bKeys)
# glutMainLoop()


#TASK 2



import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

w,h= 500,500
points= []
speed= 0.4
blinking= False
frozen= False
box_size= 200
seed= 42
def my_random():
    global seed
    seed= (1103515245*seed+12345)&0x7FFFFFFF
    return seed/0x7FFFFFFF

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    drawTheBox()
    drawThePoints()

    glutSwapBuffers()

def drawTheBox():
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(-box_size, -box_size); glVertex2f(box_size, -box_size)
    glVertex2f(box_size, -box_size); glVertex2f(box_size, box_size)
    glVertex2f(box_size, box_size); glVertex2f(-box_size, box_size)
    glVertex2f(-box_size, box_size); glVertex2f(-box_size, -box_size)
    glEnd()

def keyboardListener(key, x, y):
    global frozen
    if key== b' ':
        frozen=not frozen

def specialKeyListener(key, x, y):
    global speed
    if frozen: return
    
    if key== GLUT_KEY_UP:
        speed+= 0.05
    if key== GLUT_KEY_DOWN:
        speed= max(0,speed-0.05)

def convert_coordinate(x,y):
    a=x-(w/2)
    b=(h/2)-y 
    return a,b

blink_timer= 0
def animate():
    global blink_timer
    if frozen: return

    #blinking
    if blinking:
        blink_timer+=1
        if blink_timer>30:
            blink_timer=0
            for p in points:
                p['visible']=not p['visible']
    
    #move
    for p in points:
        p['x']+=p['dx']*speed
        p['y']+=p['dy']*speed

        #bounce
        if p['x']>box_size or p['x']<-box_size:
            p['dx']*=-1
        if p['y']>box_size or p['y']<-box_size:
            p['dy']*=-1

    glutPostRedisplay()

def drawThePoints():
    glPointSize(8.0)
    for p in points:
        if p['visible']:
            glColor3f(p['r'],p['g'],p['b'])
            glBegin(GL_POINTS)
            glVertex2f(p['x'],p['y'])
            glEnd()

def mouseListener(button,state, x,y):
    global blinking,blink_timer
    if frozen: return

    if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
        blinking =not blinking
        blink_timer= 0
        if not blinking:
            for p in points:
                p['visible']= True
    
    if button==GLUT_RIGHT_BUTTON and state==GLUT_DOWN:
        px,py= convert_coordinate(x, y)
        
        if-box_size<px<box_size and -box_size<py <box_size:
            dx_dir=1
            if my_random()<0.5:
                dx_dir=-1
            
            dy_dir=1
            if my_random()<0.5:
                dy_dir=-1

            new_point={
                'x':px,'y':py,
                'dx': dx_dir,'dy':dy_dir,
                'r':my_random(),'g':my_random(),'b': my_random(),
                'visible': True
            }
            points.append(new_point)

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-w/2, w/2, -h/2, h/2)

glutInit([])
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(w, h)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow(b"Task 2")
init()
print("Controls: Right Click(New Point),Left Click(Blink),Arrows(Speed),Space(Freeze)")

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
