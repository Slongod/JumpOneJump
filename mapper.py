import pygame
import time
import render
import character
def read_map(name:str):
    # 读入地图
    env = []; text = []; epainter = []; tpainter = []
    file = open(name , "r")
    make_tuple = lambda s: tuple(float(x) for x in s.split(','))
    while(True):
        s = file.readline()
        if (s == 'end'):
            break

        s = s.split()
        assert len(s) == 6

        if s[0] == 'BOX': # BOX
            env.append(character.box(posx = int(s[1]) , posy = int(s[2]) , lenx = int(s[3]) , leny = int(s[4]), tp = make_tuple(s[5][1:-1])))
            epainter.append(character.box_painter(bind_box = env[-1] , color = make_tuple(s[5][1:-1])))
        else:
            text.append(character.text(posx = int(s[1]) , posy = int(s[2]) , text = s[3] , size = int(s[4])))
            tpainter.append(character.text_painter(bind_text = text[-1] , color = make_tuple(s[5][1:-1])))

    return (env , text , epainter , tpainter)

def save(name:str , env , epainter):
    file = open(name , "w")
    for i in range(0 , len(env)):
        b = env[i]; col = epainter[i].getcol()
        scolor = str(col)
        scolor = scolor.replace(' ' , '')
        if type(b) == character.box:
            file.write(str('BOX ' + str(b.posx) + ' ' + str(b.posy) + ' ' + str(b.lenx) + ' ' + str(b.leny) + ' ' + scolor) + '\n')
        elif type(b) == character.text:
            file.write(str('TEXT ' + str(b.posx) + ' ' + str(b.posy) + ' ' + str(b.text) + ' ' + str(b.size) + ' ' + scolor) + '\n')
            
    file.write('end')
    file.close()


if __name__ == "__main__":
    # 初始化 pygame
    pygame.init()
    screen = pygame.display.set_mode((render._screen_width , render._screen_height))
    pygame.display.set_caption("move2dDemo_mapmaker")
    clock = pygame.time.Clock()
    pygame.display.update()

    # 初始化相关量
    base_len = render._screen_width / 70 # 分辨率坐标 / 游戏坐标
    width = render._screen_width / base_len # 横向显示长度
    height = render._screen_height / base_len # 纵向显示长度
    centerpos = (width * 0.5 , height * 0.3)

    env , e2 , epainter , p2 = read_map("map.move2dmap")
    env.extend(e2); epainter.extend(p2)

    player_start = character.box(posx = 0 , posy = 0 , lenx = 1 , leny = 1)
    player_start_painter = character.box_painter(bind_box = player_start , color = (0, 47, 167))
    nowobj = None; nowid = None
    if (len(env) != 0):
        nowobj = env[0]
        nowid = 0


    collst = [character.WHITE , character.RED , character.GOLD , character.GREEN]
    # 执行
    lstime = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                c = pygame.key.name(event.key)
                if c == 'i':
                    env.append(character.box())
                    nowid = len(env) - 1
                    epainter.append(character.box_painter(bind_box = env[-1] , color = character.WHITE))
                    nowobj = env[-1]
                elif c == 'u':
                    env.append(character.text(input('输入文本内容，然后按下回车：')))
                    nowid = len(env) - 1
                    epainter.append(character.text_painter(bind_text = env[-1] , color = character.WHITE))
                    nowobj = env[-1]
                elif nowid != -1 and nowobj != None:
                    if c in ['w','a','s','d'] and nowobj != None:
                        if c == 'w':
                            nowobj.posy += 1
                        if c == 'a':
                            nowobj.posx -= 1
                        if c == 's':
                            nowobj.posy -= 1
                            
                        if c == 'd':
                            nowobj.posx += 1
                    elif c in ['up','left','down','right'] and nowobj != None:
                        if type(nowobj) == character.box:
                            if c == 'up':
                                nowobj.leny += 1
                            if c == 'left':
                                nowobj.leny = max(nowobj.lenx - 1 , 0)
                            if c == 'down':
                                nowobj.leny = max(nowobj.leny - 1 , 0)
                            if c == 'right':
                                nowobj.lenx += 1
                        elif type(nowobj) == character.text:
                            if c in ['up' , 'right']:
                                nowobj.size += 1
                            else:
                                nowobj.size = max(1 , nowobj.size - 1)
                    elif c in ['o','p']:
                        if c == 'o':
                            if (nowid - 1 >= 0 and len(env) > nowid - 1):
                                nowid -= 1; nowobj = env[nowid]
                        else:
                            if (nowid + 1 < len(env)):
                                nowid += 1; nowobj = env[nowid]
                    elif c == 'y' and type(epainter[nowid]) in (character.box_painter , character.text_painter):
                        id = 0
                        while collst[id] != epainter[nowid].getcol():
                            id += 1
                        id = (id + 1) % 4
                        epainter[nowid].setcol(collst[id])
                    elif c == 't':
                        env.remove(nowobj)
                        epainter.remove(epainter[nowid])
                        del nowobj
                        if len(env) != 0:
                            nowid = min(nowid , len(env) - 1)
                            nowobj = env[nowid]
                        else:
                            nowobj = None
                            nowid = -1
                
            if (event.type == pygame.QUIT):
                save('map.move2dmap' , env , epainter)
                exit()
        print(len(env))
        # 更新对象状态
        lstime = time.time()

        # 更新显示
        screen.fill((0 , 0 , 0))
        my_painter = [player_start_painter.get_draw()]
        for ep in epainter:
            my_painter.append(ep.get_draw())
        if (nowobj != None):
            render.draw(screen , my_painter , base_len , nowobj.getpos() , centerpos)
        else:
            render.draw(screen , my_painter , base_len , (0 , 0) , centerpos)

        pygame.display.update()