import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

gL= 300
spd= 5
bSpd= 10
eSpd= .1
mxMis=10

pPos=[0,0]
pAng=90.0
pLife=5
gScr=0
misB=0
gO =False
pFall =0

blt =[]
enm = []

camH= 150.0
camA =0.0
fp =False

cht =False
cv =False

def rst():
    global pPos,pAng,pLife,gScr,misB,gO,pFall
    pPos = [0,0]
    pAng = 90
    pLife = 5
    gScr = 0
    misB = 0
    gO = False
    pFall = 0
    blt.clear()
    enm.clear()
    for i in range(5):
        spwn()

def spwn(i = None):
    global enm
    ne = {
        "pos":[random.uniform(-gL,gL),10,random.uniform(-gL,gL)],
        "size":1.0,
        "sd":1
    }
    if i!=None and i<len(enm):
        enm[i] = ne
    else:
        enm.append(ne)

def txt(x,y,s,f = GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0,1000,0,800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x,y)
    for ch in s:
        glutBitmapCharacter(f,ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def grd():
    sz = 20
    for i in range(-gL,gL,sz):
        for j in range(-gL,gL,sz):
            if (i//sz + j//sz) % 2 == 0:
                glColor3f(1,1,1)
            else:
                glColor3f(0.8,0.7,1.0)
            glBegin(GL_QUADS)
            glVertex3f(i,0,j)
            glVertex3f(i+sz,0,j)
            glVertex3f(i+sz,0,j+sz)
            glVertex3f(i,0,j+sz)
            glEnd()

def wall():
    h = 50
    # back wall
    glColor3f(0,0.8,0.8)
    glBegin(GL_QUADS)
    glVertex3f(-gL,0,-gL)
    glVertex3f(gL,0,-gL)
    glVertex3f(gL,h,-gL)
    glVertex3f(-gL,h,-gL)
    glEnd()
    # right wall
    glColor3f(0,1,0)
    glBegin(GL_QUADS)
    glVertex3f(gL,0,-gL)
    glVertex3f(gL,0,gL)
    glVertex3f(gL,h,gL)
    glVertex3f(gL,h,-gL)
    glEnd()
    # left wall
    glColor3f(0,0,1)
    glBegin(GL_QUADS)
    glVertex3f(-gL,0,-gL)
    glVertex3f(-gL,0,gL)
    glVertex3f(-gL,h,gL)
    glVertex3f(-gL,h,-gL)
    glEnd()

def ply():
    glPushMatrix()
    glTranslatef(pPos[0],25,pPos[1])
    glRotatef(pAng,0,1,0)

    if gO:
        glRotatef(pFall,1,0,0)

    q = gluNewQuadric()

    # torso
    glColor3f(0.4,0.5,0.3)
    glPushMatrix()
    glTranslatef(0,8,0)
    glScalef(2.2,3.2,1.4)
    glutSolidCube(10)
    glPopMatrix()

    # head
    glColor3f(0,0,0)
    glPushMatrix()
    glTranslatef(0,25,0)
    glutSolidSphere(8,20,20)
    glPopMatrix()

    # gun
    glColor3f(0.7,0.7,0.7)
    glPushMatrix()
    glTranslatef(0,12,10)
    gluCylinder(q,4.5,4.5,20,20,20)
    # gun tip
    glTranslatef(0,0,20)
    gluCylinder(q,3.5,0,6,20,20)
    glPopMatrix()

    # left hand
    glColor3f(1,0.85,0.7)
    glPushMatrix()
    glTranslatef(-12,12,5)
    gluCylinder(q,4.5,4.5,15,10,10)
    glPopMatrix()

    # right hand
    glColor3f(1,0.85,0.7)
    glPushMatrix()
    glTranslatef(12,12,5)
    gluCylinder(q,4.5,4.5,15,10,10)
    glPopMatrix()

    # left leg
    glColor3f(0,0,0.8)
    glPushMatrix()
    glTranslatef(-9,-3,0)
    glRotatef(90,1,0,0)
    gluCylinder(q,5.5,5.5,25,10,10)
    glPopMatrix()

    # right leg
    glPushMatrix()
    glTranslatef(9,-3,0)
    glRotatef(90,1,0,0)
    gluCylinder(q,5.5,5.5,25,10,10)
    glPopMatrix()

    glPopMatrix()

def enmD():
    for e in enm:
        glPushMatrix()
        glTranslatef(e['pos'][0],e['pos'][1],e['pos'][2])
        glScalef(e['size'],e['size'],e['size'])

        # body
        glColor3f(1,0,0)
        glutSolidSphere(8,20,20)

        # eye
        glColor3f(0,0,0)
        glPushMatrix()
        glTranslatef(0,0,8)
        glutSolidSphere(2,10,10)
        glPopMatrix()

        glPopMatrix()

def gunF():
    glPushMatrix()
    glTranslatef(5,-5,-15)
    glRotatef(-5,0,1,0)

    q = gluNewQuadric()

    # gun barrel
    glColor3f(0.7,0.7,0.7)
    gluCylinder(q,2.5,2.5,30,16,16)

    # gun tip
    glPushMatrix()
    glTranslatef(0,0,30)
    gluCylinder(q,2.5,0,8,16,16)
    glPopMatrix()

    # right hand
    glColor3f(1,0.85,0.7)
    glPushMatrix()
    glTranslatef(3,-3,5)
    gluSphere(q,4,16,16)
    glPopMatrix()

    # left hand
    glColor3f(1,0.85,0.7)
    glPushMatrix()
    glTranslatef(-3,-3,5)
    gluSphere(q,4,16,16)
    glPopMatrix()

    glPopMatrix()
def bltD():
    glColor3f(1,1,0)
    for b in blt:
        glPushMatrix()
        glTranslatef(b['pos'][0],b['pos'][1],b['pos'][2])
        glutSolidCube(4)
        glPopMatrix()

def keyb(k,x,y):
    global pAng,cht,cv

    if gO:
        if k==b'r' or k==b'R':
            rst()
        return

    r = math.radians(pAng)
    nx = pPos[0]
    nz = pPos[1]

    if k==b'w' or k==b'W':
        nx += spd * math.sin(r)
        nz += spd * math.cos(r)

    if k==b's' or k==b'S':
        nx -= spd * math.sin(r)
        nz -= spd * math.cos(r)

    if -gL < nx < gL and -gL < nz < gL:
        pPos[0] = nx
        pPos[1] = nz

    if k==b'a' or k==b'A':
        pAng = (pAng + 5) % 360

    if k==b'd' or k==b'D':
        pAng = (pAng - 5) % 360

    if k==b'c' or k==b'C':
        cht = not cht

    if k==b'v' or k==b'V':
        if cht:
            cv = not cv

def spKey(k,x,y):
    global camH,camA
    if k==GLUT_KEY_UP:
        camH += 5
    if k==GLUT_KEY_DOWN:
        camH -= 5
    if k==GLUT_KEY_LEFT:
        camA -= 3
    if k==GLUT_KEY_RIGHT:
        camA += 3

def mbtn(b,s,x,y):
    global fp

    if not gO:
        if b==GLUT_LEFT_BUTTON and s==GLUT_DOWN:
            r = math.radians(pAng)
            mz = 36
            sx = pPos[0] + mz * math.sin(r)
            sz = pPos[1] + mz * math.cos(r)

            blt.append({
                "pos":[sx,37,sz],
                "dir":[math.sin(r),math.cos(r)],
                "lifespan":100
            })

    if b==GLUT_RIGHT_BUTTON and s==GLUT_DOWN:
        fp = not fp

def cam():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90,1.25,1,1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if fp:
        r = math.radians(pAng)
        hy = 50
        ef = 4

        ex = pPos[0] + ef * math.sin(r)
        ey = hy
        ez = pPos[1] + ef * math.cos(r)

        ld = 80
        lx = ex + ld * math.sin(r)
        ly = ey
        lz = ez + ld * math.cos(r)

        gluLookAt(ex,ey,ez,lx,ly,lz,0,1,0)
    else:
        r = math.radians(camA)
        cx = 350 * math.sin(r)
        cz = 350 * math.cos(r)
        gluLookAt(cx,camH,cz,0,0,0,0,1,0)

def idle():
    global misB,pLife,gScr,gO,pAng,pFall

    if gO:
        if pFall < 90:
            pFall += 1
        glutPostRedisplay()
        return

    # bullet move
    rm = []
    for i,b in enumerate(blt):
        b['pos'][0] += b['dir'][0]*bSpd
        b['pos'][2] += b['dir'][1]*bSpd
        b['lifespan'] -= 1

        if b['lifespan']<=0 or not(-gL<b['pos'][0]<gL and -gL<b['pos'][2]<gL):
            rm.append(i)
            misB += 1

    for i in sorted(rm,reverse=True):
        del blt[i]

    # enemy move + size change
    for e in enm:
        dx = pPos[0]-e['pos'][0]
        dz = pPos[1]-e['pos'][2]
        d = math.sqrt(dx*dx + dz*dz)

        if d!=0:
            e['pos'][0] += dx/d*eSpd
            e['pos'][2] += dz/d*eSpd

        e['size'] += e['sd']*0.02
        if e['size']>1.5 or e['size']<0.5:
            e['sd'] *= -1

    # bullet hit enemy
    rm = []
    resp = []
    for i,b in enumerate(blt):
        for j,e in enumerate(enm):
            if j in resp:
                continue
            d = math.sqrt((b['pos'][0]-e['pos'][0])**2 + (b['pos'][2]-e['pos'][2])**2)
            if d < 10*e['size']:
                if i not in rm:
                    rm.append(i)
                resp.append(j)
                gScr += 1

    for i in sorted(rm,reverse=True):
        if i<len(blt):
            del blt[i]

    for j in set(resp):
        spwn(j)

    # player hit enemy
    hit = []
    for j,e in enumerate(enm):
        d = math.sqrt((pPos[0]-e['pos'][0])**2 + (pPos[1]-e['pos'][2])**2)
        if d < 20:
            pLife -= 1
            hit.append(j)
            if pLife <= 0:
                gO = True
                break

    if not gO:
        for j in set(hit):
            spwn(j)

    # cheat mode
    if cht and not gO:
        pAng = (pAng + 2) % 360
        for e in enm:
            dx = e['pos'][0]-pPos[0]
            dz = e['pos'][2]-pPos[1]
            a = math.degrees(math.atan2(dx,dz)) % 360
            dif = abs(pAng-a)
            if min(dif,360-dif) < 5 and random.random()<0.1:
                r = math.radians(pAng)
                sx = pPos[0] + 36*math.sin(r)
                sz = pPos[1] + 36*math.cos(r)
                blt.append({
                    "pos":[sx,37,sz],
                    "dir":[math.sin(r),math.cos(r)],
                    "lifespan":100
                })

    # game over check
    if misB>=mxMis or pLife<=0:
        gO = True

    glutPostRedisplay()

def scr():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    cam()
    grd()
    wall()

    if not fp:
        ply()
    else:
        gunF()

    enmD()
    bltD()

    # hud
    txt(10,770,"Life: " + str(max(0,pLife)))
    txt(10,740,"Score: " + str(gScr))
    txt(10,710,"Missed: " + str(misB))

    if gO:
        txt(400,400,"GAME OVER",GLUT_BITMAP_TIMES_ROMAN_24)
        txt(380,370,"Press R",GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()

def main():
    glutInit()
    rst()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000,800)
    glutInitWindowPosition(100,100)
    glutCreateWindow(b"noob bullet game")

    glutDisplayFunc(scr)
    glutKeyboardFunc(keyb)
    glutSpecialFunc(spKey)
    glutMouseFunc(mbtn)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__=="__main__":
    main()
