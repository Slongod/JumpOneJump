import pygame
import time
import character
import render

if __name__ == "__main__":
    # 初始化 pygame
    pygame.init()
    screen = pygame.display.set_mode((render._screen_width , render._screen_height))
    pygame.display.set_caption("move2dDemo")
    clock = pygame.time.Clock()
    pygame.display.update()

    # 初始化游戏相关量
    base_len = render._screen_width / 40 # 分辨率坐标 / 游戏坐标
    width = render._screen_width / base_len # 横向显示长度
    height = render._screen_height / base_len # 纵向显示长度
    centerpos = (width * 0.5 , height * 0.3)
    pactor = character.player(posx = 0 , posy = 0)
    ppainter = character.player_painter(bind_player = pactor , color = character.BLUE)
    pctrller = character.player_controller(bind_player = pactor)
    env , text , epainter , tpainter = read_map("map.move2dmap")
    
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

        my_painter = []
        for tp in tpainter:
            my_painter.append(tp.get_draw())
        for ep in epainter:
            my_painter.append(ep.get_draw())
        my_painter.append(ppainter.get_draw(env))
        render.draw(screen , my_painter , base_len , pactor.getpos() , centerpos)

        pygame.display.update()