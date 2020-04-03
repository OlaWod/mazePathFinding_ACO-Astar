from random import randint

matrix = []     # 整个地图矩阵
num_x = 50      # 横着能摆50个方块
num_y = 60      # 竖着能摆60个方块
wall_num = 1200     # 墙最多1200个
spawnX, spawnY = 0,0# 出生点，起点
foodX, foodY = 0,0  # 食物点，终点

pheromone_init = 1.0# 初始信息素量

# 是否能放置
def canPut(x,y): 
    if type(matrix[x][y]) == str:
        return False
    
    if y+1 < num_y and type(matrix[x][y+1]) != str:
        return True
    if y-1 > 0 and type(matrix[x][y-1]) != str:
        return True
    if type(matrix[x+1][y]) != str:
        return True
    if x+1 < num_x and y+1 < num_y and type(matrix[x+1][y+1]) != str:
        return True
    if x+1 < num_x and y-1 > 0 and type(matrix[x+1][y-1]) != str:
        return True
    if x-1 > 0 and type(matrix[x-1][y]) != str:
        return True
    if x-1 > 0 and y+1 < num_y and type(matrix[x-1][y+1]) != str:
        return True
    if x-1 > 0 and y-1 > 0 and type(matrix[x-1][y-1]) != str:
        return True
    
    return False

# 地图初始化
def initMatrix(): 
    matrix.clear()
    
    for i in range(num_x):
        matrix.append([])
        matrix[i] = [pheromone_init]*num_y  # 初始化地图上每个格子的信息素量

    for i in range(wall_num):
        wallX = randint(0, num_x-1)
        wallY = randint(0, num_y-1)
        matrix[wallX][wallY] = "wall"    # 墙壁

    global spawnX
    global spawnY
    while True:
        spawnX = randint(0, num_x-1)
        spawnY = randint(0, num_y-1)
        if canPut(spawnX, spawnY):
            matrix[spawnX][spawnY] = "spawn"    # 出生点
            break

    global foodX
    global foodY
    while True:
        foodX = randint(0, num_x-1)
        foodY = randint(0, num_y-1)
        if canPut(foodX, foodY):
            matrix[foodX][foodY] = "food"    # 食物点
            break

if __name__=='__main__':
    initMatrix()
    for x in matrix:
        print(x)
