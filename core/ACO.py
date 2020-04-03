from random import choice
from random import random
import maze
from maze import (pheromone_init, matrix, num_x, num_y)

ant_num = 2000      # 蚂蚁数量
elite_ratio = 0.002  # 蚂蚁中精英的比例为0.2%
ants = []

# 算法相关
alpha = 3   # 信息素残留信息的相对重要程度系数
beta = 3    # 启发信息，这里即与终点的距离，的相对重要程度系数
pheromone_food = 1000 * pheromone_init  # 食物点的信息素
pheromone_spawn = 1 * pheromone_init  # 出生点的信息素
evaporate_rate = 0.005  # 蒸发系数
k = 0.03    # 影响蚂蚁身上的信息素含量的系数

# 蚂蚁类
class Ant:
    def __init__(self, spawnX,spawnY):
        self.x = spawnX
        self.y = spawnY
        self.is_elite = False
        length = ((spawnX - maze.foodX)**2 + (spawnY - maze.foodY)**2) ** 0.5   # 起点与终点距离
        self.pheromone = (pheromone_init * length) / (ant_num * k) # 蚂蚁身上的信息素含量，找到食物后释放
        
        self.find_food = False  # 是否找到食物
        self.possible_dires = []    # 能走的方向
        self.possible_dires_notobu = []    # 能走的方向,包括之前走过的路
        self.tabu_list = [] # 禁忌表，存放之前走过的路
        self.tabu_list_index = 0    # 走到第几个回头路
        self.dict = 0     # 已经走过的路径长度
        self.dict_total = 0 # 总路径长度

    # dire：方向direction，0-7，0为向上，顺时针方向
    def move(self,dire):
        if [self.x, self.y] not in self.tabu_list:
            self.tabu_list.append([self.x, self.y]) # 当前位置加入禁忌表

        dx, dy = 0, 0

        if dire == 0:
            dy = -1
        elif dire == 1:
            dy = -1
            dx = 1
        elif dire == 2:
            dx = 1
        elif dire == 3:
            dx = 1
            dy = 1
        elif dire == 4:
            dy = 1
        elif dire == 5:
            dy = 1
            dx = -1
        elif dire == 6:
            dx = -1
        elif dire == 7:
            dx = -1
            dy = -1
        
        self.x += dx
        self.y += dy
		
        if [self.x, self.y] not in self.tabu_list:  # 当前位置加入禁忌表
            self.tabu_list.append([self.x, self.y])

        if (dx * dy == 0):  # 走直线
            self.dict += 1
        else:               # 走对角线
            self.dict += 2 ** 0.5

    # 去下一个位置
    def turn(self):
        # 这只蚂蚁还未曾找到食物
        if not self.find_food:
            # 可能的方向
            if (self.x == 0) and (self.y == 0):
                self.addPossibleDires([2, 3, 4])
            if (self.x == 0) and (self.y == num_y-1):
                self.addPossibleDires([0, 1, 2])
            if (self.x == num_x-1) and (self.y == 0):
                self.addPossibleDires([4, 5, 6])
            if (self.x == num_x-1) and (self.y == num_y-1):
                self.addPossibleDires([6, 7, 0])
                
            if (self.x == 0) and (self.y in range(1, num_y-1)):
                self.addPossibleDires([0, 1, 2, 3, 4])
            if (self.x == num_x-1) and (self.y in range(1, num_y-1)):
                self.addPossibleDires([0, 4, 5, 6, 7])
            if (self.y == 0) and (self.x in range(1, num_x-1)):
                self.addPossibleDires([2, 3, 4, 5, 6])
            if (self.y == num_y-1) and (self.x in range(1, num_x-1)):
                self.addPossibleDires([6, 7, 0, 1, 2])
            if (self.x in range(1, num_x-1)) and (self.y in range(1, num_y-1)):
                self.addPossibleDires([0, 1, 2, 3, 4, 5, 6, 7])

            if len(self.possible_dires) == 0:   # 走入死胡同，四周都是墙或已走过的地方
                self.possible_dires = self.possible_dires_notobu
                '''
                self.respawn()  # 重生
                return
                '''
            
            # 计算每个方向的选择概率
            total = 0   # 分母
            probabilities = []  # 选择概率
            for dire in self.possible_dires:
                total += (self.getPheromone(dire) ** alpha) * (self.getInverseDistance(dire) ** beta)
            for dire in self.possible_dires:    # 整个分数
                probabilities.append((self.getPheromone(dire) ** alpha) * (self.getInverseDistance(dire) ** beta) / total)

            # 普通蚂蚁,会不走寻常路
            if not self.is_elite:   
                # 计算end之前的概率和prob_range
                def sumElements(probabilities, end):
                    summ = 0.0
                    for i in range(end+1):
                        summ += probabilities[i]
                    return summ

                prob_range = [0.0]
                for i in range(len(probabilities)):
                    prob_range.append(sumElements(probabilities, i))
                prob_range[-1] = 1.0
                
                # 例：porrible_dires: [0,   1,   6]
                #     probabilities : [0.3, 0.5, 0.199]
                #     prob_range    : [0.0, 0.3, 0.8, 1.0]

                # 轮盘赌选一个方向
                def selectDire():
                    rand = random()
                    for i in range(len(prob_range)):
                        if rand >= prob_range[i] and rand < prob_range[i+1]:
                            return self.possible_dires[i]

                dire = selectDire()
                self.move(dire)
                
            # 精英蚂蚁，直接走最好的方向，以加速收敛
            else:
                def selectDire():
                    max_prob = max(probabilities)
                    max_indexes = []
                    for i in range(len(probabilities)):
                        if probabilities[i] == max_prob:
                            max_indexes.append(i)
                    return self.possible_dires[choice(max_indexes)]

                dire = selectDire()
                self.move(dire)

            if matrix[self.x][self.y] == 'food':
                self.dict_total = self.dict
                self.find_food = True   # 找到食物，接下来路上会释放身上的信息素

        # 这只蚂蚁已经找到食物了，原路返回
        else:
            self.tabu_list_index += 1
            new_x = self.tabu_list[-self.tabu_list_index][0]    # 走回头路
            new_y = self.tabu_list[-self.tabu_list_index][1]
            self.dict -= ((self.x-new_x)**2 + (self.y-new_y)**2) ** 0.5
            self.x = new_x
            self.y = new_y

            if type(matrix[self.x][self.y]) != str:
                # 新信息素量 = 本地蒸发掉p的比例后残余的 + 蚂蚁释放的信息素（走的越远释放的越少）
                matrix[self.x][self.y] = matrix[self.x][self.y] + self.pheromone / (self.dict_total - self.dict)

            if (matrix[self.x][self.y] == "spawn"):
                self.respawn()
                return

    # 下个格子的残留信息素量
    def getPheromone(self,dire):
        pheromoneX = self.x
        pheromoneY = self.y
        if dire == 0:
            pheromoneY = self.y - 1
        elif dire == 1:
            pheromoneY = self.y - 1
            pheromoneX = self.x + 1
        elif dire == 2:
            pheromoneX = self.x + 1
        elif dire == 3:
            pheromoneX = self.x + 1
            pheromoneY = self.y + 1
        elif dire == 4:
            pheromoneY = self.y + 1
        elif dire == 5:
            pheromoneY = self.y + 1
            pheromoneX = self.x - 1
        elif dire == 6:
            pheromoneX = self.x - 1
        elif dire == 7:
            pheromoneX = self.x - 1
            pheromoneY = self.y - 1

        if type(matrix[pheromoneX][pheromoneY]) != str:
            return matrix[pheromoneX][pheromoneY]
        elif matrix[pheromoneX][pheromoneY] == 'food':
            return pheromone_food
        else:
            return pheromone_spawn

    # 距离的倒数
    def getInverseDistance(self, dire):
        [x, y] = self.getNextLoc(dire)
        return float(1 / (0.1+((maze.foodX - x) ** 2 + (maze.foodY - y) ** 2) ** 0.5)) # 知道终点
        ''' # 不知道终点
        if (dire == 0) or (dire == 2) or (dire == 4) or (dire == 6):
            return 1.0 # 直线距离等于1
        else:
            return float(1 / 2 ** .5) # 对角线距离等于根号2
        '''
        
    # 重生
    def respawn(self):
        self.x = maze.spawnX
        self.y = maze.spawnY
        self.find_food = False
        self.dict = 0
        self.dict_total = 0
        self.tabu_list.clear()
        self.tabu_list_index = 0

    # 由方向dire得到下一个位置
    def getNextLoc(self,dire):
        if dire == 0:
            return [self.x, self.y - 1]
        elif dire == 1:
            return [self.x + 1, self.y - 1]
        elif dire == 2:
            return [self.x + 1, self.y]
        elif dire == 3:
            return [self.x + 1, self.y + 1]
        elif dire == 4:
            return [self.x, self.y + 1]
        elif dire == 5:
            return [self.x - 1, self.y + 1]
        elif dire == 6:
            return [self.x - 1, self.y]
        elif dire == 7:
            return [self.x - 1, self.y - 1]

    # 将能走的方向dire加入表possible_dires中
    def addPossibleDires(self,dire_list):
        self.possible_dires.clear()
        self.possible_dires_notobu.clear()
        
        for dire in dire_list:
            next_loc = self.getNextLoc(dire)    # 走dire这个方向会到达的位置next_loc
            
            # 1不超x边界;2不超y边界;3不是墙;   4不在禁忌表中，之前没走过
            if next_loc[0] in range(0,num_x) and next_loc[1] in range(0,num_y) and matrix[next_loc[0]][next_loc[1]] != "wall":
                self.possible_dires_notobu.append(dire)
                if  next_loc not in self.tabu_list:
                    self.possible_dires.append(dire)

# 初始化蚂蚁们
def createAnts():
    ants.clear()
    
    for i in range(ant_num):    # 共ant_num只蚂蚁
        ants.append(Ant(maze.spawnX,maze.spawnY))

    elite_num = ant_num * elite_ratio   # 精英蚂蚁数
    while elite_num > 0:    
        elite_candidate = choice(ants)  # 随机抽取一只蚂蚁成为精英
        if not elite_candidate.is_elite:
            elite_candidate.is_elite = True
            elite_num -= 1

# 蚂蚁移动
def moveAnts():
    for ant in ants:
        ant.turn()

# 全场信息素蒸发
def globalEvaporate():
    for i in range(num_x):
        for j in range(num_y):
            if type(matrix[i][j]) != str:
                matrix[i][j] *= (1-evaporate_rate)
    
        
if __name__=='__main__':
    createAnts()
    for x in ants:
        print(x.x, x.y, x.is_elite)
