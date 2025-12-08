import pygame
import character

_screen_width = 1280
_screen_height = 720
_reverse = lambda x: _screen_height - x + 1

def draw_box(screen , obj , scale):
    global _reverse
    col , pts = obj
    pygame.draw.polygon(screen , color = col , points = tuple((scale(x) , _reverse(scale(y))) for x , y in pts))

def draw_text(screen , obj , scale):
    col , (text , size , pos) = obj
    text_render = pygame.font.Font('font.ttf' , size).render(text , True , col)
    screen.blit(text_render , (scale(pos[0]) , _reverse(scale(pos[1]))))
    
def draw(screen , gotten_painter:list , base_len:float , playerpos:tuple , centerpos:tuple):
    posx , posy = playerpos; centerx , centery = centerpos
    scale = lambda x : x * base_len # 缩放函数
    for obj in gotten_painter: # obj 应为 list/tuple，包括（类型，颜色，内容）
        if obj[0] == character.POLYGON: # Polygon 内容：（点）
            draw_box(screen , (obj[1] , tuple((x - posx + centerx , y - posy + centery) for x , y in obj[2])) , scale)
        elif obj[0] == character.TEXT: # Text 内容：（文本，大小，（点））
            draw_text(screen , (obj[1] , (obj[2][0] , obj[2][1] , (obj[2][2][0] - posx + centerx , obj[2][2][1] - posy + centery))) , scale)
