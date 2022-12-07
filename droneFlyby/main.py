import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
pygame.display.set_caption("flyby")
FPS = 15
radiusField = 15
clock = pygame.time.Clock()
borders = []
kvadrSpeed = 5

# print("Введите количество точек, задающих исследуемую область")
# amount = int(input())
# for i in range(amount):
#     print("Введите x", i)
#     x = input()
#     print("Введите y",i)
#     y = input()
#     borders.append((int(x), int(y)))

amount = 5
borders.append((float(50), float(100)))
borders.append((float(150), float(50)))
borders.append((float(450), float(400)))
borders.append((float(100), float(450)))
borders.append((float(30), float(250)))

def koffUravnK(p1, p2):
    k = (p1[1] - p2[1]) / (p1[0] - p2[0])
    return float(k)

def koffUravnB(p1, p2):
    b = p2[1] - koffUravnK(p1, p2) * p2[0]
    return float(b)

kb = []
for i in range(amount):
    if i == amount - 1:
        kb.append((koffUravnK(borders[i], borders[0]), koffUravnB(borders[i], borders[0])))
    else:
        kb.append((koffUravnK(borders[i], borders[i + 1]), koffUravnB(borders[i], borders[i + 1])))
print(kb)

dis = pygame.display.set_mode((WIDTH, HEIGHT))
game_over = False

xyCircle = borders[0]
xCircle = borders[0][0]+1
yCircle = borders[0][1]+1
sm = 0
kvadrSpeedVert = kvadrSpeed

def rotate(A, B, C):
    return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])

def pointloc(P, A):
    n = len(P)
    if rotate(P[0], P[1], A) < 0 or rotate(P[0], P[n - 1], A) > 0:
        return False

def intersect(A, B, C, D):
    return rotate(A, B, C) * rotate(A, B, D) <= 0 and rotate(C, D, A) * rotate(C, D, B) < 0

def getDistance(point,line):
    a = -kb[line][0]
    c = - kb[line][1]
    dist = abs(a*point[0]+point[1]+c)/pow(pow(a,2)+1,0.5)
    return dist

global distCheck
distCheck = 0
global jet
jet = False

parallel = True
kbOne = kb[0]
while not game_over:
    dis.fill(WHITE)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    for i in range(amount - 1):
        pygame.draw.line(dis, BLACK, borders[i], borders[i + 1], 2)
        if i == amount - 2:
            pygame.draw.line(dis, BLACK, borders[i + 1], borders[0], 2)

    if parallel:
        if jet:
            kvadrSpeed = -kvadrSpeed
        xCircle += kvadrSpeed
        yCircle = kbOne[0]* xCircle + kbOne[1] + sm
        jet = False
        pygame.draw.circle(dis, GREEN, (xCircle, yCircle), radiusField)


    else:
        if kbOne[0]>0:
            xCircle+=kvadrSpeedVert
        else:
            xCircle+=-kvadrSpeedVert
        yCircle = kbOne[0] * xCircle + kbOne[1]
        pygame.draw.circle(dis, GREEN, (xCircle, yCircle), radiusField)
        parallel = True
        kbOne = kb[0]
        sm += radiusField
        distCheck = 0
        jet = True


    p, r = 1, amount - 1
    while r - p > 1:
        q = (p + r) // 2
        if rotate(borders[0], borders[int(q)], (xCircle, yCircle)) < 0:
            r = q
        else:
            p = q

    intersectWithPR = intersect(borders[0], (xCircle, yCircle), borders[int(p)], borders[int(r)])
    intersectWithOR = intersect(borders[int(p)], (xCircle, yCircle), borders[0], borders[int(r)])
    intersectWithOP = intersect(borders[int(r)], (xCircle, yCircle), borders[int(p)], borders[0])


    if intersectWithPR:

        parallel = False
        if p > r:
            if distCheck <= getDistance((xCircle, yCircle), int(r)):
                kbOne = kb[int(r)]
                distCheck = getDistance((xCircle, yCircle), int(r))
        else:
            if distCheck <= getDistance((xCircle, yCircle), int(r)):
                kbOne = kb[int(p)]
                distCheck = getDistance((xCircle, yCircle), int(p))
    elif intersectWithOR:
        parallel = False
        if r == amount-1:
            if distCheck <= getDistance((xCircle, yCircle), int(r)):
                kbOne = kb[int(r)]
                distCheck = getDistance((xCircle, yCircle), int(r))
        elif r == 1:
            if distCheck <= getDistance((xCircle, yCircle), 1):
                kbOne = kb[1]
                distCheck = getDistance((xCircle, yCircle), 1)
    elif intersectWithOP:
        parallel = False
        if r == amount - 1:
            if distCheck <= getDistance((xCircle, yCircle), int(r)):
                kbOne = kb[int(r)]
                distCheck = getDistance((xCircle, yCircle), int(r))
        elif r == 1:
            if distCheck <= getDistance((xCircle, yCircle), 1):
                kbOne = kb[1]
                distCheck = getDistance((xCircle, yCircle), 1)




    pygame.display.update()
