import pygame
import time
from character import *

_screen_width = 1280
_screen_height = 720
_reverse = lambda x: _screen_height - x + 1

def draw_box(screen , painter , scale):
    global _reverse
    col , pts = painter
    pygame.draw.polygon(screen , color = col , points = tuple((scale(x) , _reverse(scale(y))) for x , y in pts))

def draw(screen , gotten_painter:list , base_len:float , playerpos:tuple , centerpos:tuple):
    posx , posy = playerpos; centerx , centery = centerpos
    scale = lambda x : x * base_len # 缩放函数
    for painter in gotten_painter:
        draw_box(screen , tuple((painter[0] , tuple((x - posx + centerx , y - posy + centery) for x , y in painter[1]))) , scale)

def read_map(name:str):
    # 读入地图
    env = []; epainter = []
    file = open(name , "r")
    make_tuple = lambda s: tuple(float(x) for x in s.split(','))
    while(True):
        s = file.readline()
        if (s == 'end'):
            break
        s = s.split()
        assert (len(s) == 5)
        env.append(box(posx = int(s[0]) , posy = int(s[1]) , lenx = int(s[2]) , leny = int(s[3])))
        epainter.append(box_painter(bind_box = env[-1] , color = make_tuple(s[4][1:-1])))
    return (env , epainter)

if __name__ == "__main__":
    # 初始化 pygame
    pygame.init()
    screen = pygame.display.set_mode((_screen_width , _screen_height))
    pygame.display.set_caption("move2dDemo")
    clock = pygame.time.Clock()
    pygame.display.update()

    # 初始化游戏相关量
    base_len = _screen_width / 40 # 分辨率坐标 / 游戏坐标
    width = _screen_width / base_len # 横向显示长度
    height = _screen_height / base_len # 纵向显示长度
    centerpos = (width * 0.5 , height * 0.3)
    pactor = player(posx = 0 , posy = 0)
    ppainter = player_painter(bind_player = pactor , color = (0, 47, 167))
    pctrller = player_controller(bind_player = pactor)
    env , epainter = read_map("map.move2dmap")

    # 执行游戏
    lstime = time.time()
    while (True):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                c = pygame.key.name(event.key)
                if (c == 'r'):
                    pactor.posx , pactor.posy = 0 , 0
                else:
                    pctrller.move(c , True)
            if (event.type == pygame.KEYUP):
                c = pygame.key.name(event.key)
                pctrller.move(c , False)
            if (event.type == pygame.QUIT):
                exit()

        # 更新对象状态
        pactor.update(dtime = time.time() - lstime , boxes = env)
        ppainter.update(env)
        pctrller.update(env)
        lstime = time.time()

        # 更新显示
        screen.fill((0 , 0 , 0))
        my_painter = [ppainter.get_draw(env)]
        for ep in epainter:
            my_painter.append(ep.get_draw())
        draw(screen , my_painter , base_len , pactor.getpos() , centerpos)

        pygame.display.update()