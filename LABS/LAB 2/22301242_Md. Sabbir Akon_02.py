from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time, sys
winw = 800
winh = 600

#game states
run= True
over= False
scr= 0

#catcher
catchw= 120
catchh=24
catchx=winw//2-catchw//2
catchy=50
catchspd=1000
catchcol=(1,1,1)
catchcolred=(1,0,0)

#diamond
diasz= 16
diax= random.randint(60, winw-60)
diay= winh-80
diacol=(1,1,0)
diaspd=180.0
diaacc=10.0
dialive=True
#delta t
lastt=time.time()

#buttons
btnh= 40
btnw= 40
btny=winh-50
bre={'x':30,'y':btny,'w':btnw,'h':btnh}
bcolre=(0,0.8,0.8)
btog={'x':winw//2 - btnw//2,'y':btny,'w':btnw,'h':btnh}
bcoltog =(1,0.6,0)
bshowpause= True
bexit= {'x':winw-btnw-30,'y':btny,'w':btnw,'h':btnh}
bcolexit=(1,0,0)

#midpoint
def zone(dx,dy):
    a=abs(dx);b=abs(dy)
    if a>=b:
        if dx>=0 and dy>=0: 
            return 0
        if dx<0 and dy>=0: 
            return 3
        if dx<0 and dy<0: 
            return 4
        if dx>=0 and dy<0: 
            return 7
    else:
        if dx>=0 and dy>=0: 
            return 1
        if dx<0 and dy>=0: 
            return 2
        if dx<0 and dy<0: 
            return 5
        if dx>=0 and dy<0: 
            return 6

def to0(x,y,z):
    if z==0: 
        return x,y
    if z==1: 
        return y,x
    if z==2: 
        return y,-x
    if z==3: 
        return -x,y
    if z==4: 
        return -x,-y
    if z==5: 
        return -y,-x
    if z==6: 
        return -y,x
    if z==7: 
        return x,-y
def from0(x,y,z):
    if z==0: 
        return x,y
    if z==1: 
        return y,x
    if z==2: 
        return -y,x
    if z==3: 
        return -x,y
    if z==4: 
        return -x,-y
    if z==5: 
        return -y,-x
    if z==6: 
        return y,-x
    if z==7: 
        return x,-y

def dot(x,y):
    glBegin(GL_POINTS)
    glVertex2i(int(x),int(y))
    glEnd()

def drline(x1,y1,x2,y2):
    dx=x2-x1;dy=y2-y1
    z=zone(dx,dy)
    ax,ay=to0(x1,y1,z)
    bx,by=to0(x2,y2,z)
    if ax>bx: 
        ax,bx=bx,ax;ay,by=by,ay
    dx0=bx-ax;dy0=by-ay
    d=2*dy0-dx0
    incE=2*dy0
    incNE=2*(dy0-dx0)
    x=ax;y=ay
    ox,oy=from0(x,y,z);dot(ox,oy)
    while x<bx:
        if d>0: 
            d+=incNE;y+=1
        else: 
            d+=incE
        x+=1
        ox,oy=from0(x,y,z);dot(ox,oy)

#shapes
def drrect(x,y,w,h):
    drline(x,y,x+w,y)
    drline(x+w,y,x+w,y+h)
    drline(x+w,y+h,x,y+h)
    drline(x,y+h,x,y)

def drdia(cx,cy,s):
    t=(cx,cy+s);r=(cx+s,cy);b=(cx,cy-s);l=(cx-s,cy)
    drline(t[0],t[1],r[0],r[1])
    drline(r[0],r[1],b[0],b[1])
    drline(b[0],b[1],l[0],l[1])
    drline(l[0],l[1],t[0],t[1])

def drplay(x,y,w,h):
    p1=(x+int(0.25*w),y+int(0.2*h))
    p2=(x+int(0.25*w),y+int(0.8*h))
    p3=(x+int(0.8*w),y+int(0.5*h))
    drline(p1[0],p1[1],p2[0],p2[1])
    drline(p2[0],p2[1],p3[0],p3[1])
    drline(p3[0],p3[1],p1[0],p1[1])

def drpause(x,y,w,h):
    bar=w//3;gap=bar//2
    lx=x+gap;rx=x+2*gap+bar
    drrect(lx,y,bar,h)
    drrect(rx,y,bar,h)

def drarrow(x,y,w,h):
    tx=x+5;ty=y+h//2
    hx=x+w//3
    ht=y+h-5;hb=y+5
    drline(tx,ty,hx,ht)
    drline(tx,ty,hx,hb)
    se=x+w-5
    drline(hx,ty,se,ty)

def drx(x,y,w,h):
    drline(x,y,x+w,y+h)
    drline(x+w,y,x,y+h)

def drcatch():
    global catchx,catchy,catchw,catchh
    if over: 
        glColor3f(*catchcolred)
    else: 
        glColor3f(*catchcol)
    lb=(catchx,catchy)
    rb=(catchx+catchw,catchy)
    rt=(catchx+catchw-20,catchy+catchh)
    lt=(catchx+20,catchy+catchh)
    drline(lb[0],lb[1],rb[0],rb[1])
    drline(rb[0],rb[1],rt[0],rt[1])
    drline(rt[0],rt[1],lt[0],lt[1])
    drline(lt[0],lt[1],lb[0],lb[1])

#col detect
def aabb(x1,y1,w1,h1,x2,y2,w2,h2):
    return (x1<x2+w2 and x1+w1>x2 and y1<y2+h2 and y1+h1>y2)

def diahit():
    return (diax-diasz,diay-diasz,diasz*2,diasz*2)

def catchhit():
    return (catchx,catchy,catchw,catchh)

#logic
def reset():
    global scr,diaspd,diax,diay,diacol,dialive,over,run,bshowpause
    scr=0
    diaspd=180
    diax=random.randint(60,winw-60)
    diay=winh-80
    diacol=rcol()
    dialive=True
    over=False
    run=True
    bshowpause=True
    print("Starting Over")

def rcol():
    c=[(1,0.2,0.2),(0.2,1,0.2),(0.2,0.6,1),(1,0.8,0.2),(0.8,0.2,1),(0.2,1,1),(1,0.4,0.9)]
    return random.choice(c)

def tog():
    global run,bshowpause
    run=not run
    bshowpause=run

def quit():
    print("Goodbye (score:",scr,")")
    glutLeaveMainLoop()

def gameup(dt):
    global diay,diax,diaspd,scr,dialive,over
    if not run: return
    if over: return
    diay-=diaspd*dt
    diaspd+=diaacc*dt
    dx,dy,dw,dh=diahit()
    cx,cy,cw,ch=catchhit()
    if aabb(dx,dy,dw,dh,cx,cy,cw,ch):
        scr+=1
        print("Score:",scr)
        diax=random.randint(60,winw-60)
        diay=winh-80
        diacol=rcol()
    if diay+diasz<0:
        dialive=False
        over=True
        print("Game Over (score:",scr,")")

#draw
def drawbtn(b,c,f):
    glColor3f(*c)
    f(b['x'],b['y'],b['w'],b['h'])

def show():
    glClear(GL_COLOR_BUFFER_BIT)
    drawbtn(bre,bcolre,drarrow)
    if bshowpause: drawbtn(btog,bcoltog,drpause)
    else: drawbtn(btog,bcoltog,drplay)
    drawbtn(bexit,bcolexit,drx)
    drcatch()
    if not over:
        glColor3f(*diacol)
        drdia(diax,diay,diasz)
    glutSwapBuffers()

def idle():
    global lastt
    now=time.time()
    dt=now-lastt
    lastt=now
    gameup(dt)
    glutPostRedisplay()

#input
def key(k,x,y):
    if over or not run: return
    if k==b'\x1b': quit()

def skey(k,x,y):
    global catchx
    if over or not run: return
    mv=40
    if k==GLUT_KEY_LEFT: catchx-=mv
    elif k==GLUT_KEY_RIGHT: catchx+=mv
    if catchx<0: catchx=0
    if catchx+catchw>winw: catchx=winw-catchw

def mouse(btn,st,mx,my):
    global scr
    my=winh-my
    if btn==GLUT_LEFT_BUTTON and st==GLUT_DOWN:
        if inr(mx,my,bre): reset()
        elif inr(mx,my,btog): tog()
        elif inr(mx,my,bexit): quit()

def inr(px,py,r):
    return (px>=r['x'] and px<=r['x']+r['w'] and py>=r['y'] and py<=r['y']+r['h'])

#init
def init():
    glClearColor(0.05,0.05,0.08,1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,winw,0,winh)
    glPointSize(1)
    glMatrixMode(GL_MODELVIEW)

#run game
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB)
glutInitWindowSize(winw,winh)
glutCreateWindow(b"catch diamonds midpoint line only")
init()
lastt=time.time()
glutDisplayFunc(show)
glutIdleFunc(idle)
glutKeyboardFunc(key)
glutSpecialFunc(skey)
glutMouseFunc(mouse)
reset()
glutMainLoop()
