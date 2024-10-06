import pygame
import sys
from pygame.locals import *
import math


#todo napraw bug z prostopadlom scianom do kamery
width=700
window = pygame.display.set_mode((width, width), 0, 0)
screenz =[0,0,-250]
lig=(0,-1000,0)
cam=[0,0,-10000]
a=100
qz=0
qy=0
qx=0
def obx(point,a):
    x=point[0]
    y=math.cos(a)*point[1]-math.sin(a)*point[2]
    z=math.sin(a)*point[1]+math.cos(a)*point[2]
    return [x,y,z]

def oby(point,a):
    x=math.cos(a)*point[0]+math.sin(a)*point[2]
    y=point[1]
    z=-math.sin(a)*point[0]+math.cos(a)*point[2]
    return [x,y,z]


def obz(point,a):
    x=math.cos(a)*point[0]-math.sin(a)*point[1]
    y=math.sin(a)*point[0]+math.cos(a)*point[1]
    z=point[2]
    return [x,y,z]


p=[(qx - a, qy - a, qz - a), (qx - a, qy + a, qz - a), (qx + a, qy + a, qz - a), (qx + a, qy - a, qz - a), (qx - a, qy - a, qz + a), (qx - a, qy + a, qz + a), (qx + a, qy + a, qz + a), (qx + a, qy - a, qz + a)]
lin=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
wals=[(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def pointpos(camera,point):
    x=((screenz[2]-camera[2])/(point[2]-camera[2]))*(point[0]-camera[0])+camera[0]
    y = ((screenz[2]-camera[2]) / (point[2]-camera[2])) * (point[1] -camera[1]) +camera[1]
    return [x,y]

line_color=(1,1,1)
def conections(points,lines):
    for i  in lines:
        c=width/2
        a=[points[i[0]][0]+c-screenz[0],points[i[0]][1]+c-screenz[1]]
        b=[points[i[1]][0]+c-screenz[0],points[i[1]][1]+c-screenz[1]]
        pygame.draw.line(window, line_color, a, b)

def ilowek(a,b):
    v = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    la=(a[0]**2+a[1]**2+a[2]**2)**(1/2)
    lb=(b[0]**2+b[1]**2+b[2]**2)**(1/2)
    lv=(v[0]**2+v[1]**2+v[2]**2)**(1/2)
    sin=lv/(la*lb)
    return [v,sin]

def skalar(a,b):
    u=a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
    la=(a[0]**2+a[1]**2+a[2]**2)**(1/2)
    lb=(b[0]**2+b[1]**2+b[2]**2)**(1/2)
    cos=u/(la*lb)
    return [u,cos]

def odl(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)**(1/2)
def fill(points,wals,camera,p3d,light):
    order=[]
    for i in wals:
        x=0
        y=0
        z=0
        for j in i:
            x+=p3d[j][0]/len(i)
            y += p3d[j][1] / len(i)
            z += p3d[j][2] / len(i)
        a=(p3d[i[0]][0]-p3d[i[1]][0],p3d[i[0]][1]-p3d[i[1]][1],p3d[i[0]][2]-p3d[i[1]][2])
        b = (p3d[i[2]][0] - p3d[i[1]][0], p3d[i[2]][1] - p3d[i[1]][1], p3d[i[2]][2] - p3d[i[1]][2])
        v=ilowek(a,b)[0]
        if odl(camera,(v[0]+x,v[1]+y,v[2]+z)) > odl(camera,(-v[0]+x,-v[1]+y,-v[2]+z)):
            v=[-v[0],-v[1],-v[2]]
        d=((camera[0]-x)**2+(camera[1]-y)**2+(camera[2]-z)**2)**(1/2)

        dd=(light[0]-x,light[1]-y,light[2]-z)
        sk=skalar(v, dd)[1]
        if sk<0:
            sk=0

        order.append([d,i,sk])
    order.sort()
    order.reverse()
    a=1
    for i in order:
        c = width / 2
        poin=[(points[k][0]+c-screenz[0],points[k][1]+c-screenz[1]) for k in i[1]]
        a+=1

        pygame.draw.polygon(window,(50+(150*(i[2])),50+(150*(i[2])),50+(150*(i[2]))),poin)

pause=0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if pause==0:
                    pause = 1
                else:
                    pause=0
    window.fill("RED")
    scp=[]
    for k in p:
        scp.append(pointpos(cam,k))
    if pause == 0:
        for k in range(len(p)):
            p[k]=obx(p[k],0.0015)
        for k in range(len(p)):
            p[k]=oby(p[k],0.001)
        for k in range(len(p)):
            p[k]=obz(p[k],0.0025)
    fill(scp,wals,cam,p,lig)
    ##conections(scp,lin)
    pygame.time.wait(1)
    pygame.display.update()
