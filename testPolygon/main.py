from Polygon import *
import pygame
from GeneticAlg import *
from coverageFromGit.coverage_test import *
import time

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage


pygame.init()
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 215, 0)
pygame.display.set_caption("flyby")
FPS = 15
radiusField = 15
BATTERY_PATH = 25
clock = pygame.time.Clock()
kvadrSpeed = 5
coords = []
wx = 40 # ширина углового поля
wy = 20  # высота углового поля
#
# coords.append((float(50), float(HEIGHT-100)))
# coords.append((float(150), float(HEIGHT-150)))
# coords.append((float(450), float(HEIGHT-300)))
# coords.append((float(100), float(HEIGHT-250)))
# coords.append((float(30), float(HEIGHT-150)))
# coords.append((float(50), float(HEIGHT-90)))

# coords.append((float(50), float(HEIGHT-100)))
# coords.append((float(70), float(HEIGHT-100)))
# coords.append((float(110), float(HEIGHT-300)))
# coords.append((float(50), float(HEIGHT-300)))




coords.append((float(50), float(HEIGHT-150)))
coords.append((float(150), float(HEIGHT-120)))
coords.append((float(450), float(HEIGHT-400)))
coords.append((float(200), float(HEIGHT-450)))
coords.append((float(120), float(HEIGHT-250)))
coords.append((float(60), float(HEIGHT-200)))

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
img = maskaCoord.copy()
print(img)
for j in range(maskaCoord.shape[1]):
    if maskaCoord[0][j] == 0:
        maskaCoord[0][j] = 2
        break
start = j
for j in range(maskaCoord.shape[1]):
    if maskaCoord[maskaCoord.shape[0]-1][j] == 0:
        maskaCoord[0][j] = 2
        break
goal = j



points = np.array(points)
points = np.reshape(points,(line,int(points.shape[0]/line)))
yForStr = np.linspace(yForStr,yForStr+line*wy,line+1) #исправить
#https://github.com/rodriguesrenato/coverage-path-planning
# bestPath = getOptimalPath(maskaCoord)




do_animation = True


def transform(
        grid_map, src, distance_type='chessboard',
        transform_type='path', alpha=0.01
):
    """transform

    calculating transform of transform_type from src
    in given distance_type

    :param grid_map: 2d binary map
    :param src: distance transform source
    :param distance_type: type of distance used
    :param transform_type: type of transform used
    :param alpha: weight of Obstacle Transform used when using path_transform
    """

    n_rows, n_cols = grid_map.shape

    if n_rows == 0 or n_cols == 0:
        sys.exit('Empty grid_map.')

    inc_order = [[0, 1], [1, 1], [1, 0], [1, -1],
                 [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    if distance_type == 'chessboard':
        cost = [1, 1, 1, 1, 1, 1, 1, 1]
    elif distance_type == 'eculidean':
        cost = [1, np.sqrt(2), 1, np.sqrt(2), 1, np.sqrt(2), 1, np.sqrt(2)]
    else:
        sys.exit('Unsupported distance type.')

    transform_matrix = float('inf') * np.ones_like(grid_map, dtype=float)
    transform_matrix[src[0], src[1]] = 0
    if transform_type == 'distance':
        eT = np.zeros_like(grid_map)
    elif transform_type == 'path':
        eT = ndimage.distance_transform_cdt(1 - grid_map, distance_type)
    else:
        sys.exit('Unsupported transform type.')

    # set obstacle transform_matrix value to infinity
    for i in range(n_rows):
        for j in range(n_cols):
            if grid_map[i][j] == 1.0:
                transform_matrix[i][j] = float('inf')
    is_visited = np.zeros_like(transform_matrix, dtype=bool)
    is_visited[src[0], src[1]] = True
    traversal_queue = [src]
    calculated = [(src[0] - 1) * n_cols + src[1]]

    def is_valid_neighbor(g_i, g_j):
        return 0 <= g_i < n_rows and 0 <= g_j < n_cols \
               and not grid_map[g_i][g_j]

    while traversal_queue:
        i, j = traversal_queue.pop(0)
        for k, inc in enumerate(inc_order):
            ni = i + inc[0]
            nj = j + inc[1]
            if is_valid_neighbor(ni, nj):
                is_visited[i][j] = True

                # update transform_matrix
                transform_matrix[i][j] = min(
                    transform_matrix[i][j],
                    transform_matrix[ni][nj] + cost[k] + alpha * eT[ni][nj])

                if not is_visited[ni][nj] \
                        and ((ni - 1) * n_cols + nj) not in calculated:
                    traversal_queue.append((ni, nj))
                    calculated.append((ni - 1) * n_cols + nj)

    return transform_matrix


def get_search_order_increment(start, goal):
    if start[0] >= goal[0] and start[1] >= goal[1]:
        order = [[1, 0], [0, 1], [-1, 0], [0, -1],
                 [1, 1], [1, -1], [-1, 1], [-1, -1]]
    elif start[0] <= goal[0] and start[1] >= goal[1]:
        order = [[-1, 0], [0, 1], [1, 0], [0, -1],
                 [-1, 1], [-1, -1], [1, 1], [1, -1]]
    elif start[0] >= goal[0] and start[1] <= goal[1]:
        order = [[1, 0], [0, -1], [-1, 0], [0, 1],
                 [1, -1], [-1, -1], [1, 1], [-1, 1]]
    elif start[0] <= goal[0] and start[1] <= goal[1]:
        order = [[-1, 0], [0, -1], [0, 1], [1, 0],
                 [-1, -1], [-1, 1], [1, -1], [1, 1]]
    else:
        sys.exit('get_search_order_increment: cannot determine \
            start=>goal increment order')
    return order


def wavefront(transform_matrix, start, goal):
    """wavefront

    performing wavefront coverage path planning

    :param transform_matrix: the transform matrix
    :param start: start point of planning
    :param goal: goal point of planning
    """

    path = []
    n_rows, n_cols = transform_matrix.shape

    def is_valid_neighbor(g_i, g_j):
        is_i_valid_bounded = 0 <= g_i < n_rows
        is_j_valid_bounded = 0 <= g_j < n_cols
        if is_i_valid_bounded and is_j_valid_bounded:
            return not is_visited[g_i][g_j] and \
                   transform_matrix[g_i][g_j] != float('inf')
        return False

    inc_order = get_search_order_increment(start, goal)

    current_node = start
    is_visited = np.zeros_like(transform_matrix, dtype=bool)

    while current_node != goal:
        i, j = current_node
        path.append((i, j))
        is_visited[i][j] = True

        max_T = float('-inf')
        i_max = (-1, -1)
        i_last = 0
        for i_last in range(len(path)):
            current_node = path[-1 - i_last]  # get latest node in path
            for ci, cj in inc_order:
                ni, nj = current_node[0] + ci, current_node[1] + cj
                if is_valid_neighbor(ni, nj) and \
                        transform_matrix[ni][nj] > max_T:
                    i_max = (ni, nj)
                    max_T = transform_matrix[ni][nj]

            if i_max != (-1, -1):
                break

        if i_max == (-1, -1):
            break
        else:
            current_node = i_max
            if i_last != 0:
                print('backtracing to', current_node)
    path.append(goal)

    return path


def visualize_path(grid_map, start, goal, path):  # pragma: no cover
    oy, ox = start
    gy, gx = goal
    # px, py = np.transpose(np.flipud(np.fliplr(path)))

    px,py = np.transpose(np.fliplr(path))

    if not do_animation:
        plt.imshow(grid_map, cmap='Greys')
        plt.plot(ox, oy, "-xy")
        plt.plot(px, py, "-r")
        plt.plot(gx, gy, "-pg")
        plt.show()
    else:
        for ipx, ipy in zip(px, py):
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
            plt.imshow(grid_map, cmap='Greys')
            plt.plot(ox, oy, "-xb")
            plt.plot(px, py, "-r")
            plt.plot(gx, gy, "-pg")
            plt.plot(ipx, ipy, "or")
            plt.axis("equal")
            plt.grid(True)
            plt.pause(0.1)


# def main():
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#
#     img = plt.imread(os.path.join(dir_path, 'map', 'test.png'))
#     img = 1 - img  # revert pixel values
#     print(img.shape)

goal = (maskaCoord.shape[0]-1, goal)
start = (0,start)

print(img.shape)
    # distance transform wavefront
DT = transform(img, goal, transform_type='distance')
DT_path = wavefront(DT, start, goal)

print(f'DT_PATH: {DT_path}')
path_cost = 0
recharge = []
add_list = []
for i in range(len(DT_path)-1):
    if (abs(DT_path[i+1][0] - DT_path[i][0]) == 1) and (abs(DT_path[i+1][1] - DT_path[i][1]) == 1):
        add = np.sqrt(2)
        add_list.append(add)
        path_cost+=add
    else:
        add = 1
        add_list.append(add)
        path_cost+=add
    if path_cost >=BATTERY_PATH:
        DT_path1 = DT_path[:i + 1].copy()
        print(DT_path[i])
        bol = False
        for xy in DT_path1[::-1]:
            if bol == True:
                break
            else:
                for el in img[xy[0] - 1:xy[0] + 2, xy[1] - 1:xy[1] + 2]:
                    if bol == True:
                        break
                    else:
                        for el2 in el:
                            if el2 == 1:
                                recharge.append(xy)
                                bol = True
                                if bol:
                                    break
        index_recharge = DT_path.index(recharge[-1])
        path_cost = 0
        if index_recharge-i != 0:
            last_added_numbers = add_list[-abs(index_recharge-i):]
            for num in last_added_numbers:
                path_cost += num


# bol = False
# for xy in DT_path1[::-1]:
#     if bol == True:
#         break
#     else:
#         for el in img[xy[0] - 1:xy[0] + 2, xy[1] - 1:xy[1] + 2]:
#             if bol == True:
#                 break
#             else:
#                 for el2 in el:
#                     if el2 == 1:
#                         recharge.append(xy)
#                         bol = True
#                         break
img_with_recharge = img.copy()
#
# for el in DT_path1[:DT_path1.index((4,6))]: # change index to recharge
#     img_with_recharge[el[0]][el[1]] = 1
# PT2 = transform(img_with_recharge,goal)
# PT2_path = wavefront(PT2, (4,6), goal)
# print(PT2_path)



# visualize_path(img, start, goal, DT_path)


    # path transform wavefront
PT = transform(img, goal, transform_type='path', alpha=0.01)
PT_path = wavefront(PT, start, goal)
# visualize_path(img, start, goal, PT_path)


# if __name__ == "__main__":
#     main()

print(f'recharge: {recharge}')

while not game_over:
    dis.fill(WHITE)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    area.drawPolygon(BLACK)
    area.drawRectangularGrid(wx,wy)
    pygame.display.update()
    n = 0
    for step in DT_path:
        x1 = points[step[0], step[1]]
        y1 = yForStr[step[0]]
        if step in recharge:
            pygame.draw.rect(dis, YELLOW, (x1 - wx / 2, y1 - wy / 2, wx, wy))
        else:
            pygame.draw.rect(dis, GREEN, (x1 - wx / 2, y1 - wy / 2, wx, wy),5)

        if n == 1 :
            pygame.draw.line(dis,BLACK,beg,(x1,y1))
        time.sleep(0.1)
        pygame.display.update()
        n = 1
        beg = (x1,y1)

# print(f'Optimal path finding took {until -since:0.4f}')
# print(points)




