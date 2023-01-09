from .common.settings import *
from .common.ui_utils import *


world_map = {}

m, n = int(WINDOW_SIZE[0] * 0.01), int(WINDOW_SIZE[1] * 0.01)
area_1 = [[0]*m for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i == 0 or i == n-1 or j == 0 or j == n-1:
            area_1[i][j] = 1

pprint_matrix(area_1)

world_map[1] = area_1
