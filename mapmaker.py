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
    file.close()
    return (env , epainter)

def save(name:str , env , color):
    file = open(name , "w")
    scolor = str(color)
    scolor = scolor.replace(' ' , '')
    for b in env:
        file.write(str(str(b.posx) + ' ' + str(b.posy) + ' ' + str(b.lenx) + ' ' + str(b.leny) + ' ' + scolor) + '\n')
    file.write('end')
    file.close()


if __name__ == "__main__":
    # 初始化 pygame
    pygame.init()
    screen = pygame.display.set_mode((_screen_width , _screen_height))
    pygame.display.set_caption("move2dDemo_mapmaker")
    clock = pygame.time.Clock()
    pygame.display.update()

    # 初始化相关量
    base_len = _screen_width / 70 # 分辨率坐标 / 游戏坐标
    width = _screen_width / base_len # 横向显示长度
    height = _screen_height / base_len # 纵向显示长度
    centerpos = (width * 0.5 , height * 0.3)
    env , epainter = read_map("map.move2dmap")
    _col = (233,235,254)
    player_start = box(posx = 0 , posy = 0 , lenx = 1 , leny = 1)
    player_start_painter = box_painter(bind_box = player_start , color = (0, 47, 167))
    nowbox = None; nowid = None
    if (len(env) != 0):
        nowbox = env[0]
        nowid = 0


    # 执行
    lstime = time.time()
    while (True):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                c = pygame.key.name(event.key)
                if (c in ['w','a','s','d'] and nowbox != None):
                    if (c == 'w'):
                        nowbox.posy += 1
                    if (c == 'a'):
                        nowbox.posx -= 1
                    if (c == 's'):
                        nowbox.posy -= 1
                    if (c == 'd'):
                        nowbox.posx += 1
                elif (c in ['up','left','down','right'] and nowbox != None):
                    if (c == 'up'):
                        nowbox.leny += 1
                    if (c == 'left'):
                        nowbox.lenx -= 1
                    if (c == 'down'):
                        nowbox.leny -= 1
                    if (c == 'right'):
                        nowbox.lenx += 1
                elif (c in ['o','p']):
                    if (c == 'o'):
                        if (nowid - 1 >= 0 and len(env) > nowid - 1):
                            nowid -= 1; nowbox = env[nowid]
                    else:
                        if (nowid + 1 < len(env)):
                            nowid += 1; nowbox = env[nowid]
                elif (c == 'i'):
                    nowid = len(env) + 1
                    env.append(box())
                    epainter.append(box_painter(bind_box = env[-1] , color = _col))
                    nowbox = env[-1]
                
            if (event.type == pygame.QUIT):
                save('map.move2dmap' , env , _col)
                exit()

        # 更新对象状态
        lstime = time.time()

        # 更新显示
        screen.fill((0 , 0 , 0))
        my_painter = [player_start_painter.get_draw()]
        for ep in epainter:
            my_painter.append(ep.get_draw())
        if (nowbox != None):
            draw(screen , my_painter , base_len , nowbox.getpos() , centerpos)
        else:
            draw(screen , my_painter , base_len , (0 , 0) , centerpos)

        pygame.display.update()