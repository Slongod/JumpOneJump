import pygame
import time
import character
import render
import mapper

def player_dead(pactor:character.player , text:list , tpainter:list):
    posx , posy = pactor.getpos()
    text.append(character.text(text = 'You Died' , size = 70 , posx = posx - 10 , posy = posy + 10))
    tpainter.append(character.text_painter(bind_text = text[-1] , color = character.RED))
    text.append(character.text(text = '请按 R 键复活' , size = 40 , posx = posx - 10 , posy = posy + 6))
    tpainter.append(character.text_painter(bind_text = text[-1] , color = character.RED))

def player_relive(pactor:character.player , text:list , tpainter:list):
    pactor.posx , pactor.posy = (0 , 0)
    pactor.relive()
    text.remove(text[-1]); text.remove(text[-1])
    tpainter.remove(tpainter[-1]); tpainter.remove(tpainter[-1])

if __name__ == "__main__":
    # 初始化 pygame
    pygame.init()
    screen = pygame.display.set_mode((render._screen_width , render._screen_height))
    pygame.display.set_caption("蹦一蹦")
    clock = pygame.time.Clock()
    pygame.display.update()

    # 初始化游戏相关量
    base_len = render._screen_width / 40 # 分辨率坐标 / 游戏坐标
    width = render._screen_width / base_len # 横向显示长度
    height = render._screen_height / base_len # 纵向显示长度
    centerpos = (width * 0.5 , height * 0.3)
    pactor = character.player(posx = 0 , posy = 0 , gold = (2 , 4 , 5))
    ppainter = character.player_painter(bind_player = pactor , color = character.BLUE)
    pctrller = character.player_controller(bind_player = pactor)

    map_len = 4; now_mapid = 0
    env , text , epainter , tpainter = mapper.read_map("map0.move2dmap")
    
    # 执行游戏
    is_player_alive = True
    lstime = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                c = pygame.key.name(event.key)
                if not is_player_alive and c == 'r':
                    is_player_alive = True
                    player_relive(pactor , text , tpainter)
                elif is_player_alive:
                    pctrller.move(c , True)
            if event.type == pygame.KEYUP:
                if is_player_alive:
                    c = pygame.key.name(event.key)
                    pctrller.move(c , False)
            if event.type == pygame.QUIT:
                exit()

        # 更新对象状态
        pactor.update(dtime = time.time() - lstime , boxes = env)
        ppainter.update(env)
        pctrller.update(env)
        lstime = time.time()

        if pactor.success:
            now_mapid += 1
            env , text , epainter , tpainter = mapper.read_map("map{}.move2dmap".format(now_mapid))
            pactor.posx , pactor.posy = (0 , 0)
            pactor.relive()
            pactor.success = False

        # 更新显示
        screen.fill((0 , 0 , 0))

        my_painter = []
        for ep in epainter:
            my_painter.append(ep.get_draw())
        for tp in tpainter:
            my_painter.append(tp.get_draw())
        my_painter.append(ppainter.get_draw(env))
        render.draw(screen , my_painter , base_len , pactor.getpos() , centerpos)

        pygame.display.update()
        if is_player_alive and pactor.is_dead():
            is_player_alive = False
            player_dead(pactor , text , tpainter)