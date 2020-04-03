from maze import matrix
import maze

class Node:
    def __init__(self, parent, x, y, dist):
        self.parent = parent    # 前一个节点
        self.x = x
        self.y = y
        self.dist = dist    # 已经走过的路径长度

open = []
close = []
path = []

# 寻路
def findPath():
    open.clear()
    close.clear()
    path.clear()
    
    p = Node(None, maze.spawnX, maze.spawnY, 0.0)   # 起始节点
    while True:
        extendAround(p)  # 将四周可行节点加入open表

        if open == []:  # open表为空，接下来无路可走，失败退出
            return

        i, p = getBest()    # 获得open表中最好的节点p及其索引i
        if found(p):   # 找到终点，成功退出
            makePath(p) # 构造路径
            return

        close.append(p)
        del open[i]

# 判断是否找到终点(maze.foodX, maze.foodY)
def found(p):
    return p.x == maze.foodX and p.y == maze.foodY

# 构造路径
def makePath(p):
    while p:
        path.append((p.x, p.y))
        p = p.parent

# 获得open表中最好的节点p及其索引i
def getBest():
    best_f = maze.num_x * maze.num_y     # 整个地图绕一圈也就这么长
    best_i = -1
    best_p = None
    for i in range(len(open)):
        f = open[i].dist + heuristic(open[i])   # f = g + h
        if f < best_f:  # 更优
            best_f = f
            best_i = i
            best_p = open[i]
    return best_i, best_p

# 从节点p到终点(maze.foodX, maze.foodY)的接近程度的估计
def heuristic(p):
    return 1 * ((maze.foodX-p.x)**2 + (maze.foodY-p.y)**2)**0.5

# 将四周可行节点加入open表
def extendAround(parent):
    dx_list = (-1, 0, 1, -1, 1, -1, 0, 1)
    dy_list = (-1,-1,-1,  0, 0,  1, 1, 1)

    for dx, dy in zip(dx_list, dy_list):
        new_x, new_y = parent.x + dx, parent.y + dy

        if isValid(new_x, new_y):  # 新地点有效

            length = 1  # 两点间距离
            if dx*dy != 0:
                length = 2**0.5
                
            p = Node(parent, new_x, new_y, parent.dist+length)
            i = getOpenIndex(new_x, new_y)  # 获取这个地点在open表中的位置
            if i != -1: # 这个地点在open表中
                if p.dist < open[i].dist:   # 当前路径更短
                    open[i].parent = p
                    open[i].dist = p.dist
                continue
            else:   # 新节点
                open.append(p)
            
# 判断(x,y)是否是有效地点
def isValid(x, y):
    if x<0 or x>=maze.num_x or y<0 or y>=maze.num_y:  # 超界
        return False

    if matrix[x][y] == 'wall':   # 是墙
        return False

    for p in close: # 在close表中
        if p.x == x and p.y ==y:
            return False
        
    return True # 有效

# 获取地点(x, y)在open表中的位置
def getOpenIndex(x, y):
    for i in range(len(open)):
        if open[i].x == x and open[i].y == y:
            return i
    return -1 # 不在open表中

if __name__=='__main__':
    maze.initMatrix()
    findPath()
    print(path)
    print(maze.spawnX, maze.spawnY)
    print(maze.foodX, maze.foodY)
