import math
import time
# 默认单位
# 时间：s，长度：m，加速度：m/s^2，力：N，弹性系数：N/m

# 默认正方向
# 向右、向上

#定义常量
UP = 1
DOWN = -1
RIGHT = 2
LEFT = -2
NOTHING = 0
POLYGON = 'POLYGON'
TEXT = 'TEXT'
X = 0
Y = 1
PI = math.acos(-1)
WHITE = (233 , 235 , 254)
BLUE = (0 , 47 , 167)
GOLD = (255 , 215 , 0)
RED = (255 , 0 , 127)
GREEN = (0 , 128 , 128)


# 获取 op 方向的反向
def reverse(op: int):
    return -op
# 计算 (x,y) 绕 (x0,y0) 旋转 alpha（弧度）得到的新点
def rotate(x:float , y:float , x0:float , y0:float , alpha:float):
    _x = x0 + (x - x0) * math.cos(alpha) - (y - y0) * math.sin(alpha)
    _y = y0 + (x - x0) * math.sin(alpha) + (y - y0) * math.cos(alpha)
    return (_x , _y)

# 矩形物体
class box:
    def __init__(self , lenx:float = 1 , leny:float = 1 , posx:float = 0 , posy:float = 0):
        # 长宽
        self.lenx = lenx
        self.leny = leny

        # 中心点坐标
        self.posx = posx
        self.posy = posy

    def left(self):
        return self.posx - self.lenx / 2
    def right(self):
        return self.posx + self.lenx / 2
    def down(self):
        return self.posy - self.leny / 2
    def up(self):
        return self.posy + self.leny / 2
    def getpos(self):
        return (self.posx , self.posy)
    def getlen(self):
        return (self.lenx , self.leny)


# 返回 a 离 b 的哪个表面最近及距离
def go_check(a:box , b:box):
    mn = abs(a.right() - b.left()); mnid = LEFT
    if (abs(a.left() - b.right()) < mn):
        mn = abs(a.left() - b.right())
        mnid = RIGHT
    if (abs(a.up() - b.down()) < mn):
        mn = abs(a.up() - b.down())
        mnid = DOWN
    if (abs(a.down() - b.up()) < mn):
        mn = abs(a.down() - b.up())
        mnid = UP
    return (mnid , mn)

# 若重叠，返回 a 离 b 的哪个表面最近及距离；否则返回 NOTHING
def check_over(a:box , b:box):
    if (max(a.left() , b.left()) <= min(a.right() , b.right()) and max(a.down() , b.down()) <= min(a.up() , b.up())):
        return go_check(a , b)
    return NOTHING

# 玩家角色
class player(box):
    #定义函数
    # init
    def __init__(self , m:float = 1 , 
               run:tuple = (200.0 , 200.0) , jump:float = (20 , 0.15) , 
               g:float = 200 , posx:float = 0 , posy:float = 0 , 
               stopv:float = 0.1 , max_run_speed:float = 10 , max_down_speed:float = 30):
        self.__m = m # 质量
        self.__info_run = run # (加速度，阻力加速度）
        self.__info_jump = jump # (跳跃速度，最大跳跃加速时间)
        self.__g = g # 重力加速度
        box.__init__(self , 1 , 1 , posx , posy) # 初始化物理属性
        self.__stopv = stopv # 若玩家速度小于当前值，则停止
        self.__max_run_speed = max_run_speed # 玩家行走的最快速度
        self.__max_down_speed = max_down_speed # 玩家跳跃、坠落的最快速度

        self.__v = [0] * 2 # X，Y 轴上的速度
        self.__is_jumping = False # 是否正在跳跃恒定速度阶段
        self.__running = NOTHING # (NOTHING 无操作，否则为 RIGHT 或 LEFT)
        self.__last_jump_starting_time = NOTHING

    # 获取 x 方向的加速度
    def __get_xa(self):
        if (self.__running == LEFT):
            return -self.__info_run[0]
        elif (self.__running == RIGHT):
            return self.__info_run[0]
        else:
            if (self.__v[X] < 0):
                return self.__info_run[1]
            elif (self.__v[X] > 0):
                return -self.__info_run[1]
        return 0
    
    # to painter
    def get_last_jump_starting_time(self):
        return self.__last_jump_starting_time
    def is_jumping(self):
        return self.__is_jumping
    def get_running_to_num(self):
        if (self.__running == NOTHING):
            return 0
        if (self.__running == RIGHT):
            return 1
        if (self.__running == LEFT):
            return -1
    def get_max_run_speed(self):
        return self.__max_run_speed
    def get_xspeed(self):
        return self.__v[X]

    def startjump(self):
        self.__is_jumping = True
        self.__last_jump_starting_time = time.time()
    
    def stopjump(self):
        self.__is_jumping = False
    
    def startrun(self , op:int):
        assert (op in [LEFT , RIGHT])
        self.__running += op
    
    def stoprun(self , op:int):
        assert (op in [LEFT , RIGHT])
        self.__running -= op

    def is_on_ground(self , boxes:list):
        for b in boxes:
            op = check_over(self , b)
            if (op != NOTHING and op[0] == UP):
                return True
        return False

    def update(self , dtime:float , boxes:list):
        # 更新横向运动
        xa = self.__get_xa(); orig_v = self.__v[X]
        self.posx += self.__v[X] * dtime + 0.5 * xa * dtime * dtime
        self.__v[X] += xa * dtime

        # 防止摩擦力过大在一个 tick 里产生反向加速度
        if ((orig_v >= 0) != (self.__v[X] >= 0) and self.__running == NOTHING):
            self.__v[X] = 0 
        # 限速
        if (self.__v[X] > self.__max_run_speed):
            self.__v[X] = self.__max_run_speed
        if (self.__v[X] < -self.__max_run_speed):
            self.__v[X] = -self.__max_run_speed
        # 低速自动停止
        if (abs(self.__v[X]) < self.__stopv and self.__running == NOTHING):
            self.__v[X] = 0
        
        # 更新竖向运动
        if (time.time() - self.__last_jump_starting_time >= self.__info_jump[1]):
            self.stopjump()
        if (self.__is_jumping):
            self.__v[Y] = self.__info_jump[0]
            self.posy += self.__info_jump[0] * dtime
        elif (self.is_on_ground(boxes) == False):
            g = self.__g
            self.posy += self.__v[Y] * dtime - 0.5 * g * dtime * dtime
            self.__v[Y] -= g * dtime
        # 限速
        if (self.__v[Y] > self.__max_down_speed):
            self.__v[Y] = self.__max_down_speed
        if (self.__v[Y] < -self.__max_down_speed):
            self.__v[Y] = -self.__max_down_speed

        #检测碰撞
        for b in boxes:
            op = check_over(self , b)
            if (op != NOTHING):
                if (op[0] in [LEFT , RIGHT]):
                    self.__v[X] = 0
                    if (op[0] == LEFT):
                        self.posx = b.left() - (self.lenx / 2)
                    elif (op[0] == RIGHT):
                        self.posx = b.right() + (self.lenx / 2)
                else:
                    self.__v[Y] = 0
                    if (op[0] == UP):
                        self.posy = b.up() + (self.leny / 2)
                    elif (op[0] == DOWN):
                        self.posy = b.down() - (self.leny / 2)

class text:
    def __init__(self , text:str = '' , size:int = 20 , posx:int = 0 , posy:int = 0):
        self.text = text
        self.size = size
        self.posx = posx
        self.posy = posy
    def getpos(self):
        return (self.posx , self.posy)

class text_painter:
    def __init__(self , bind_text:text , color:tuple = WHITE):
        self.__bind_text = bind_text
        self.__color = color
    def get_draw(self):
        return (TEXT , self.__color , (self.__bind_text.text , self.__bind_text.size , self.__bind_text.getpos()))

class box_painter:
    def __init__(self , bind_box:box , color:tuple = WHITE):
        self.__bind_box = bind_box
        self.__color = color
    def get_draw(self):
        left = self.__bind_box.left()
        right = self.__bind_box.right()
        up = self.__bind_box.up()
        down = self.__bind_box.down()
        return (POLYGON , self.__color , ((left , down) , (right , down) , (right , up) , (left , up)))
        

class player_painter:
    def __init__(self , 
                 bind_player:player , 
                 down_scale:tuple = (0.15 , 
                               lambda x : 1 + 0.10 * math.sin(x * math.pi) , 
                               lambda x : 1 - 0.25 * math.sin(x * math.pi)
                               ) , 
                 jump_scale:tuple = (0.95 , 1.05) , 
                 run_rot:float = 4 , 
                 color:tuple = WHITE):
        self.__bind_player = bind_player
        self.__down_scale = down_scale
        self.__jump_scale = jump_scale
        self.__run_rot = run_rot / 180 * PI
        self.__last_down_time = NOTHING # 最后一次落地的时间
        self.__last_jump_time = NOTHING # 最后一次起跳的时间
        self.__mem_on_ground = True
        self.__color = color
    
    def debug_get_ltime(self):
        return self.__last_down_time
    def debug_set_last_down_time(self , x:float):
        self.__last_down_time = x
    
    def update(self , boxes):
        if (self.__bind_player.is_on_ground(boxes)):
            if (self.__mem_on_ground == False):
                self.__last_down_time = time.time()
                self.__mem_on_ground = True
        else:
            self.__mem_on_ground = False
        self.__last_jump_time = self.__bind_player.get_last_jump_starting_time()

    def get_draw(self , boxes):
        lenx , leny = self.__bind_player.getlen()

        # 落地
        down_max_time = self.__down_scale[0]
        dtime = time.time() - self.__last_down_time
        if (dtime <= down_max_time and self.__bind_player.is_on_ground(boxes)):
            lenx *= self.__down_scale[1](dtime / down_max_time)
            leny *= self.__down_scale[2](dtime / down_max_time)

        # 跳跃
        dtime = time.time() - self.__last_jump_time
        if (self.__bind_player.is_jumping()):
            lenx *= self.__jump_scale[0]#(min(dtime , jump_max_time) / jump_max_time)
            leny *= self.__jump_scale[1]#(min(dtime , jump_max_time) / jump_max_time)
        
        down = self.__bind_player.down()
        up = down + leny
        left = self.__bind_player.posx - lenx / 2
        right = self.__bind_player.posx + lenx / 2

        pts = ((left , down) , (right , down) , (right , up) , (left , up))
        pts = tuple(rotate(x , y , (left + right) / 2 , down , self.__bind_player.get_running_to_num() * self.__run_rot) for x , y in pts)

        return (POLYGON , self.__color , pts)

class player_controller:
    def __init__(self , bind_player:player , 
                 left_key:tuple = ('a' , 'left') , 
                 right_key:tuple = ('d' , 'right') , 
                 jump_key:tuple = ('space',) , 
                 jump_buffer_time:float = 0.05 , 
                 coyote_time:float = 0.05):
        self.__bind_player = bind_player
        self.__left_key = left_key
        self.__right_key = right_key
        self.__jump_key = jump_key
        self.__jump_buffer_time = jump_buffer_time # 跳跃缓存时间
        self.__coyote_time = coyote_time # 野狼时间
        self.__last_pressed_jump_time = NOTHING # 最后按缓存的跳跃的时间
        self.__last_on_ground_time = NOTHING # 最后处于地面上的时间
    
    def move(self , key:str , is_keydown:bool):
        nowtime = time.time()
        if (is_keydown):
            if (key in self.__left_key):
                self.__bind_player.startrun(LEFT)
            if (key in self.__right_key):
                self.__bind_player.startrun(RIGHT)
            if (key in self.__jump_key):
                self.__last_pressed_jump_time = nowtime
        else:
            if (key in self.__left_key):
                self.__bind_player.stoprun(LEFT)
            if (key in self.__right_key):
                self.__bind_player.stoprun(RIGHT)
            if (key in self.__jump_key):
                self.__last_pressed_jump_time = NOTHING
    def update(self , boxes:list = []):
        nowtime = time.time()
        if (self.__bind_player.is_on_ground(boxes)):
            self.__last_on_ground_time = nowtime
        
        if (nowtime - self.__last_pressed_jump_time <= self.__jump_buffer_time
            and nowtime - self.__last_on_ground_time <= self.__coyote_time):
            self.__bind_player.startjump()
        if (self.__last_pressed_jump_time == NOTHING and self.__bind_player.is_jumping()):
            self.__bind_player.stopjump()

if __name__ == "__main__":
    a = player(posx = 1.6 , posy = 0)
    b = box(1 , 1 , 1 , 0)
    a.update(boxes = [b,] , dtime = 0)
    print(a.getpos())