from Polygon import *
import pygame
from GeneticAlg import *
from coverageFromGit.coverage_test import *


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
kvadrSpeed = 5
coords = []
wx = 40 # ширина углового поля
wy = 40  # высота углового поля

coords.append((float(50), float(HEIGHT-100)))
coords.append((float(150), float(HEIGHT-50)))
coords.append((float(450), float(HEIGHT-400)))
coords.append((float(100), float(HEIGHT-450)))
coords.append((float(30), float(HEIGHT-250)))
coords.append((float(50), float(HEIGHT-100)))








# print("Введите количество точек, задающих исследуемую область")
# amountPoints = int(input())
# for i in range(amountPoints):
#     print("Введите x", i)
#     x = input()
#     print("Введите y",i)
#     y = input()
#     coords.append((int(x), int(y)))

dis = pygame.display.set_mode((WIDTH, HEIGHT))
game_over = False
area = Polygon2(coords,dis)

since = time.perf_counter()
popSize=10
mutationRate=0.05


# points = geneticAlgorithm(population=area.drawRectangularGrid(wx,wy), popSize=popSize, eliteSize=2, mutationRate=mutationRate, generations=5000)
# until = time.perf_counter()

points,line,yForStr,maskaCoord = area.drawRectangularGrid(wx,wy)

maskaCoord = np.array(maskaCoord)
maskaCoord = np.reshape(maskaCoord,(line,int(maskaCoord.shape[0]/line)))
maskaCoord[0,1] = 2

points = np.array(points)
points = np.reshape(points,(line,int(points.shape[0]/line)))
yForStr = np.linspace(yForStr,yForStr+line*wy,line+1) #исправить
getOptimalPath(maskaCoord)










while not game_over:
    dis.fill(WHITE)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    area.drawPolygon(BLACK)
    area.drawRectangularGrid(wx,wy)
    # for i in range (len(points)-2):
    #     pygame.draw.line(dis,BLACK,(points[i].x,points[i].y),(points[i+1].x,points[i+1].y))
    # pygame.draw.line(dis, BLACK, (points[len(points)-1].x, points[len(points)-1].y), (points[0].x, points[0].y))

    # for i in range(len(self.coords) - 1):
    #     pygame.draw.line(self.dis, color, self.coords[i], self.coords[i + 1], 2)
    #     if i == len(self.coords) - 2:
    #         pygame.draw.line(self.dis, color, self.coords[i + 1], self.coords[0], 2)

    pygame.display.update()





print(f'Optimal path finding took {until -since:0.4f}')
# print(points)




