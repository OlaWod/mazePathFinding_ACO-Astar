import pygame
from pygame.locals import (K_SPACE, K_UP, KEYDOWN, QUIT)
import maze
from maze import matrix
import ACO
import Astar

class App:
    def __init__(self, WIDTH, HEIGHT, TEXT_HEIGHT, SCALE):
        pygame.init()
        pygame.display.set_caption("走迷宫")

        self.SCALE = SCALE
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.TEXT_HEIGHT = TEXT_HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT+TEXT_HEIGHT))

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PINK = (255, 0, 255)
        self.LIGHTBLUE = (0, 255, 255)
        self.GREY = (20, 20, 20)
        
        self.screen.fill(self.WHITE)
        pygame.draw.line(self.screen, self.BLACK, (self.WIDTH/2, 0), (self.WIDTH/2, self.HEIGHT), 3)

        self.clock = pygame.time.Clock()
  
    # 暂停
    def pause(self):    
        self.showText("press 'space' to play")
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:    # 按空格恢复
                        return True
                elif event.type == pygame.QUIT: # 退出
                    return False

    # 画地图
    def drawMap(self):    
        self.screen.fill(self.WHITE)   # 背景
        self.showText("press 'space' to pause, press 'up' to reset")

   
        for i in range(maze.num_x): # 画信息素，出生点，食物点，墙
            for j in range(maze.num_y):
                
                if type(matrix[i][j]) != str:   # 信息素
                    grey = 255 - (matrix[i][j] - maze.pheromone_init) * 1.4    # RGB,R、B分量.信息素越多颜色越绿
                    green = 2*grey
                    if grey > 255:
                        grey = 255
                    if grey < 0:
                        grey = 0
                    if green > 255:
                        green = 255
                    if green < 50:
                        green = 50
                    self.drawPoint((grey,green,grey), i, j, True, False)

                elif matrix[i][j] == "wall":    # 墙
                    self.drawPoint(self.YELLOW, i, j, True, True)
                    
        for ant in ACO.ants:
            if not ant.is_elite:    # 普通蚂蚁
                self.drawPoint(self.PINK, ant.x, ant.y, True, False)
            else:   # 精英蚂蚁
                self.drawPoint(self.RED, ant.x, ant.y, True, False)

        for p in Astar.path:   # A*算法的路径
            self.drawPoint(self.PINK, p[0], p[1], False, True)

        self.drawPoint(self.BLUE, maze.spawnX, maze.spawnY, True, True)   # 出生点
        self.drawPoint(self.LIGHTBLUE, maze.foodX, maze.foodY, True, True)# 食物点
                    
        pygame.draw.line(self.screen, self.BLACK, (self.WIDTH/2, 0), (self.WIDTH/2, self.HEIGHT), 3)

    # 画一个正方形点
    def drawPoint(self,color,x,y,left,right):
        surf = pygame.Surface((self.SCALE, self.SCALE))  # 正方形点的大小
        surf.fill(color)   # 颜色
        rect = surf.get_rect()
        if left:    # 画左边
            self.screen.blit(surf, (x*self.SCALE, y*self.SCALE))  # 显示位置
        if right:   # 画右边
            self.screen.blit(surf, (self.WIDTH/2+x*self.SCALE, y*self.SCALE))  # 显示位置
                    
    # 显示提示文字
    def showText(self,text):    
        bar = pygame.Surface((self.WIDTH, self.TEXT_HEIGHT))  # 字的背景条的大小
        bar.fill(self.BLACK)   # 颜色
        rect = bar.get_rect()
        self.screen.blit(bar, (0, self.HEIGHT))  # 显示位置

        font = pygame.font.Font('freesansbold.ttf',self.TEXT_HEIGHT*2//3)  # 字体和大小
        TextSurface = font.render(text, True, self.WHITE)    # 要显示的字和颜色
        TextRect = TextSurface.get_rect()
        TextRect.center = ((self.WIDTH/2),(self.HEIGHT+self.TEXT_HEIGHT/2)) # 显示位置
        self.screen.blit(TextSurface, TextRect)

    def run(self):
        maze.initMatrix()
        ACO.createAnts(maze.spawnX,maze.spawnY)
        Astar.findPath()
        running = self.pause()  # 刚开始先暂停
        
        while running:
            for event in pygame.event.get():
                
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:    # 按空格暂停
                        running = self.pause()
                    elif event.key == K_UP:     # 按向上重置
                        maze.initMatrix()
                        ACO.createAnts(maze.spawnX,maze.spawnY)
                        Astar.findPath()
                
                elif event.type == pygame.QUIT: # 退出
                    running = False

            
            self.drawMap()
            pygame.display.flip()   # 画
            # --------------
            ACO.moveAnts()
            ACO.globalEvaporate()
            # --------------
            self.clock.tick()

        pygame.quit()   # 退出循环后，结束


if __name__=='__main__':
    SCALE = 10  # 每个方块的边长
    WIDTH = maze.num_x * SCALE * 2
    HEIGHT = maze.num_y * SCALE
    TEXT_HEIGHT = 60
    App(WIDTH, HEIGHT, TEXT_HEIGHT, SCALE).run()
