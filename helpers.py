# some useful 'tecnical' function

from random import randint
from math import cos, sin, pi


from vertex import Vertex

def random_rgb():
    g=randint(0,255)
    r=randint(0,255)
    b=randint(0,255)
    return (r,g,b)

def init_polygon(n, x, y, width, height, offset):
    '''
    Return a regular n-polygon that fits in window of dimensions (width, height), with an offset from the borders.
    '''
    if n==0:
        return []
    
    if n==1:
        return [Vertex(width//2, height//2)]

    x, y = x + offset, y + offset
    width, height = width - 2*offset, height - 2*offset
    delta_angle = 360 / n
    polygon = []
    angles = []
    for i in range(n):
        angles.append((45+i*delta_angle) * pi / 180 if n==4 else (90+i*delta_angle) * pi / 180)
    
    # scaling and traslating the poligon
    minX, maxX = min([cos(t) for t in angles]), max([cos(t) for t in angles])
    minY, maxY = min([sin(t) for t in angles]), max([sin(t) for t in angles])
    
    r = min((width)/(maxX-minX), (height)/(maxY-minY))

    for t in angles:
        Dy = (height - (maxY+abs(minY))*r)/2
        polygon.append(
            Vertex((x + width/2) + cos(t)*r,
                y -sin(t)*r + maxY*r + Dy)
        )
    
    return polygon