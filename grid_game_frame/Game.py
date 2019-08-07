#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configparser
import pygame
import sys
from abc import ABC, abstractmethod
import time
import random
import threading

class File:
    def _exist_file(self,file_name):
        try:
            open(file_name)
        except:
            return False
        else:
            return True
    def _open_file(self,file_name):
        if self.exist_file(file_name):
            return open(file_name)
        else:
            return False
    def _close_file(self,file):
        try:
            file.close()
        except:
            return False
        else:
            return True
class ConfigFile(File):
    def __init__(self,config_file_name,encoding = 'utf8'):
        self._config = configparser.ConfigParser()
        self._config.read(config_file_name, encoding=encoding)
        if self._config.sections() == []:
            raise("游戏配置文件内容丢失:",config_file_name)
    def get_section(self):
        return self._config.sections()
    def get_option(self,section):
        return self._config.options(section)
    def get_items(self,section):
        return self._config.items(section)
    def has_section(self,section):
        return self._config.has_section(section)
    def has_option(self,option):
        return self._config.has_section(option)
    def get_option_value(self,section,option):
        try:
            container = self._config.get(section,option)
        except:
            raise('配置值异常:',section,option)
        return container
    def get_option_value_dict(self,section):
        config_dict = {}
        common_option = self.get_option(section)
        for item in common_option:
            config_dict[item] = self.get_option_value(section,item)
        return config_dict
    def set_option_value(self,section,option,value):
        try:
            self._config.set(section,option,value)
            file = self._open_file(self.__config_file_name)
            self._config.write(file)
            self._close_file(self.__config_file_name)
            return True
        except:
            return False

class CommonGameConfig(ConfigFile):
    def __init__(self,config_file_name,encoding = 'utf8'):
        ConfigFile.__init__(self,config_file_name,encoding =encoding)
        self.__common_section = 'Common'
        self.common_config_dict = self.get_option_value_dict(self.__common_section)
    def window_x_y(self):
        x = int(self.common_config_dict['display_x'])
        y = int(self.common_config_dict['display_y'])
        return x,y
    def game_name(self):
        return self.common_config_dict['game_name']
    def game_caption(self):
        return self.common_config_dict['game_caption']
    def game_valid_keyboard(self):
        return self.common_config_dict['valid_keyboard']
    def game_background_color(self):
        return self.common_config_dict['background_color']
    def game_region(self):
        top_left_x = int(self.common_config_dict['game_region_top_lef_x'])
        top_left_y = int(self.common_config_dict['game_region_top_lef_y'])
        game_region_width = int(self.common_config_dict['game_region_width'])
        game_region_height = int(self.common_config_dict['game_region_height'])
        return top_left_x,top_left_y,game_region_width,game_region_height
    def game_region_has_frame(self):
        return self.common_config_dict['game_region_has_frame']
    def game_region_frame_color(self):
        return self.common_config_dict['game_region_frame_color']

class Color:
    def __init__(self):
        self.color = {}
        self.color['WHITE'] = (255, 255, 255)
        self.color['GRAY'] = (185, 185, 185)
        self.color['BLACK'] = (0, 0, 0)
        self.color['RED'] = (155, 0, 0)
        self.color['LIGHTRED'] = (175, 20, 20)
        self.color['GREEN'] = (0, 155, 0)
        self.color['LIGHTGREEN'] = (20, 175, 20)
        self.color['BLUE'] = (0, 0, 155)
        self.color['LIGHTBLUE'] = (20, 20, 175)
        self.color['YELLOW'] = (155, 155, 0)
        self.color['LIGHTYELLOW'] = (175, 175, 20)
        self.color['white'] = (255, 255, 255)
        self.color['gray'] = (185, 185, 185)
        self.color['black'] = (0, 0, 0)
        self.color['red'] = (155, 0, 0)
        self.color['lightred'] = (175, 20, 20)
        self.color['green'] = (0, 155, 0)
        self.color['lightgreen'] = (20, 175, 20)
        self.color['blue'] = (0, 0, 155)
        self.color['lightblue'] = (20, 20, 175)
        self.color['yellow'] = (155, 155, 0)
        self.color['lightyellow'] = (175, 175, 20)
        self.cuscolor = {}
    def COLOR(self,index):
        return self.color[index]

class ChessGameConfig(ConfigFile):
    def __init__(self,config_file_name,encoding = 'utf8'):
        ConfigFile.__init__(self,config_file_name,encoding =encoding)
        self.__score_section = 'Score'
        self.__chess_game_section = 'ChessGame'
        self.score_config_dict = self.get_option_value_dict(self.__score_section)
        self.chess_game_section = self.get_option_value_dict(self.__chess_game_section)

    def chess_height_width(self):
        height = int(self.chess_game_section['chess_height'])
        width = int(self.chess_game_section['chess_width'])
        return height, width
    def blank_postion(self):
        return self.chess_game_section['blank_position']
    def set_highest_score(self,value):
        thisvalue = str(value)
        if thisvalue.isnumeric():
            return self.set_option_value('Score','highest_score',thisvalue)
        else:
            raise("必须为数字")

class PyGame(Color,ABC):
    def __init__(self,config_file_name):
        Color.__init__(self)
        self.__common_config = CommonGameConfig(config_file_name = config_file_name)
        pygame.init()
        self.screen = pygame.display.set_mode((self.common_config().window_x_y()))
        self.set_caption(self.common_config().game_caption())
        self.set_screen_backgroud(self.COLOR(self.common_config().game_background_color()))
    def common_config(self):
        return self.__common_config
    def draw_rect(self,color, pos, width):
        pygame.draw.rect(self.screen, color, pos, width)
    def draw_line(self,color, start_pos,end_pos):
        pygame.draw.line(self.screen, color,start_pos,end_pos,1)
    def set_screen_backgroud(self,color):
        self.screen.fill(color)
    def game_region(self):
        return self.common_config().game_region()
    def set_game_area_backgroud(self,color):
        self.draw_rect(color,self.common_config().game_region(),0)
    def set_caption(self,content):
        pygame.display.set_caption(content)
    def display_update(self):
        pygame.display.update()
    def draw_grid(self,lt_x,lt_y,br_x,br_y,color = "black"):
        self.draw_line(self.COLOR(color), (lt_x, lt_y), (lt_x, br_y))
        self.draw_line(self.COLOR(color), (lt_x, lt_y), (br_x, lt_y))
        self.draw_line(self.COLOR(color), (br_x, lt_y), (lt_x, br_y))
        self.draw_line(self.COLOR(color), (lt_x, br_y), (lt_x, br_y))
    def draw_grids(self,x_num,y_num,lt_x,lt_y,br_x,br_y,color = "black"):
        width = (br_x - lt_x)/x_num
        height = (br_y - lt_y)/y_num
        for num_x in range(0,x_num + 1):
            self.draw_line(self.COLOR(color), (lt_x + width * num_x, lt_y),(lt_x + width * num_x, br_y))
        for num_y in range(0,y_num + 1):
            self.draw_line(self.COLOR(color), (lt_x, lt_y + height * num_y),(br_x, lt_y + height * num_y))

    @abstractmethod
    def init_func(self):
        pass

    @abstractmethod
    def main_func(self):
        pass

    @abstractmethod
    def event_func(self, event):
        pass

    def __screen_loop(self):
        self.init_func()
        # 程序主循环
        while True:
            # 获取事件
            for event in pygame.event.get():
                # 事件处理
                self.event_func(event)
            # 绘制屏幕
            self.main_func()
            # 更新屏幕
            self.display_update()
    def start(self):
        self.__screen_loop()


    def exit(self):
        # 退出pygame
        pygame.quit()
        # 退出系统
        sys.exit()

class ChessData:
    def __init__(self,chess_height,chess_width,init_value_chess='.'):
        self.__height = chess_height
        self.__width = chess_width
        self.__init_value_chess = init_value_chess
        self.__chess = []
        #self.__chess = ['.', '.', '.', '.',
        #                '.', '.', '.', '.',
        #                '.', '.', '.', '.',
        #                '.', '.', '.', '.']
        self.reset_chess(self.__init_value_chess)
    def reset_chess(self,value):
        self.__chess = []
        for x in range(0,self.__width*self.__height):
                self.__chess.append(value)
    def height(self):
        return self.__height
    def width(self):
        return self.__width
    def get_value(self,x,y):
        if self.isoutrange(x,y) == True:
            raise("超出范围")
        return self.__chess[self.__width*y+x]
    def set_value(self,x,y,value):
        if self.isoutrange(x,y) == True:
            raise("超出范围")
        self.__chess[self.__width*y+x] = value
    def has_value(self,x,y,value):
        if self.isoutrange(x,y) == True:
            raise("超出范围")
        if  self.__chess[self.__width*y+x] == value:
            return True
        else:
            return False
    #def left_postion(self,x,y):

    def isoutrange(self,x,y):
        if(x<0 or y<0):
            return True
        if(x>=self.__width or y>=self.__height):
            return True
        return False
    def isempty(self,x,y):
        if self.isoutrange(x,y) == True:
            raise("超出范围")
        if self.get_value(x,y) == self.__init_value_chess:
            return True
        else:
            return False

class Game(PyGame):
    def __init__(self,config_file_name):
        PyGame.__init__(self,config_file_name = config_file_name)
        self.__chess_config = ChessGameConfig(config_file_name = config_file_name)
        self.__init_frame_data()
        self._chess_data = ChessData(self.__chess_x_grid_num, self.__chess_x_grid_num, self.chess_config().blank_postion())
    def chess(self):
        return self._chess_data
    def chess_config(self):
        return self.__chess_config
    def __init_frame_data(self):
        self.__chess_x_grid_num, self.__chess_y_grid_num = self.chess_config().chess_height_width()
        self.__area_ltx, self.__area_lty, self.__area_width, self.__area_height = self.game_region()
        self.__area_brx, self.__area_bry = self.__area_ltx + self.__area_width, self.__area_lty + self.__area_height
        self.__grid_width = self.__area_width / self.__chess_x_grid_num
        self.__grid_height = self.__area_height / self.__chess_y_grid_num
    def size_grid(self):
        return self.__grid_width,self.__grid_height
    def size_game_area(self):
        return self.__area_width, self.__area_height
    def pos_game_area(self):
        return self.__area_ltx, self.__area_lty, self.__area_brx, self.__area_bry
    def num_grid(self):
        return self.__chess_x_grid_num, self.__chess_y_grid_num

    @abstractmethod
    def main_func(self):
        pass
    @abstractmethod
    def init_func(self):
        pass
    @abstractmethod
    def event_func(self, event):
        pass



class SimpleChessGame(PyGame):
    def __init__(self, config_file_name):
        PyGame.__init__(self, config_file_name)
        self.chess_config = ChessGameConfig(config_file_name=config_file_name)
        self.__init_frame_data()
        self.init_chess_frame()
        self.chess = ChessData(self.chess_x_num, self.chess_y_num, self.chess_config.blank_postion())

    def __init_frame_data(self):
        self.blank_position = self.chess_config.blank_postion()
        self.chess_x_num, self.chess_y_num = self.chess_config.chess_height_width()
        self.chess_lt_x, self.chess_lt_y, self.chess_area_width, self.chess_area_height = self.game_region()
        self.chess_br_x, self.chess_br_y = self.chess_lt_x + self.chess_area_width, self.chess_lt_y + self.chess_area_height
        self.grid_width = self.chess_area_width / self.chess_x_num
        self.grid_height = self.chess_area_height / self.chess_y_num
    def init_chess_frame(self):
        self.draw_grids(self.chess_x_num,self.chess_y_num,self.chess_lt_x,self.chess_lt_y,self.chess_br_x,self.chess_br_y)

    def fill_grid_all(self, x, y, color):
        self.draw_rect(color, (self.chess_lt_x + self.grid_width * x, self.chess_lt_y + self.grid_height * y, self.grid_width,self.grid_height), 0)


    def init_func(self):
        pass

    def main_func(self):
        self.set_screen_backgroud(self.COLOR(self.common_config().game_background_color()))
        #self.set_game_area_backgroud(self.COLOR(self.common_config().game_region_frame_color()))
        self.init_chess_frame()
        self.main_function()
        for x in range(0, self.chess.width()):
            for y in range(0, self.chess.height()):
                value = self.chess.get_value(x, y)
                self.fillgrid_function(x, y, value)

    def event_func(self, event):
        # 事件是否为退出事件
        if event.type == pygame.QUIT:
            self.exit()
        return self.event_function(event)

    @abstractmethod
    def main_function(self):
        pass
    @abstractmethod
    def event_function(self, event):
        pass
    @abstractmethod
    def fillgrid_function(self, x, y, value):
        pass

class MazeGame(SimpleChessGame):
    def __init__(self, config_file_name):
        SimpleChessGame.__init__(self, config_file_name)
        self.init_game_data()
    def main_function(self):
        pass
    def fillgrid_function(self, x, y, value):
        if value == self.GRID['MainPos']:
            self.fill_grid_all(x, y, self.COLOR("green"))
        elif value == self.GRID['RoadBlock']:
            self.fill_grid_all(x, y, self.COLOR("black"))
        elif value == self.GRID['Destination']:
            self.fill_grid_all(x, y, self.COLOR("red"))
    def go_postion(self,x,y):
        if self.chess.isoutrange(x,y) == True:
            return self.STATE['OutRange']
        postion_value = self.chess.get_value(x, y)
        if postion_value == self.GRID['Blank']:
            self.chess.set_value(self.pos_x, self.pos_y, self.GRID['Blank'])
            self.pos_x = x
            self.pos_y = y
            self.chess.set_value(self.pos_x, self.pos_y, self.GRID['MainPos'])
            return self.STATE['MoveSucc']
        elif postion_value == self.GRID['Destination']:
            self.reset_chess()
            return self.STATE['Win']
        elif postion_value == self.GRID['RoadBlock']:
            return self.STATE['MoveBolck']
    def go_left(self):
        result = self.go_postion(self.pos_x-1,self.pos_y)
        return result
    def go_up(self):
        result = self.go_postion(self.pos_x,self.pos_y-1)
        return result
    def go_down(self):
        result = self.go_postion(self.pos_x,self.pos_y+1)
        return result
    def go_right(self):
        result = self.go_postion(self.pos_x+1, self.pos_y)
        return result
    def init_game_data(self):
        self.STATE = {'MoveSucc':'MoveSucc','Win':'Win','OutRange':'OutRange','MoveBolck':'MoveBolck'}
        self.GRID = {'Blank':self.blank_position,'MainPos':'1','RoadBlock':'2','Destination':'3'}
        self.reset_chess()

    def reset_chess(self):
        self.chess.reset_chess(self.GRID['Blank'])
        self.start_pos_x = 4
        self.start_pos_y = 4
        self.pos_x = 4
        self.pos_y = 4
        self.end_pos_x = 0
        self.end_pos_y = 0

        self.block_list = [(1,1),(1,2),(0,1),(2,2),]
        #起点
        self.chess.set_value(self.start_pos_x, self.start_pos_y, self.GRID['MainPos'])
        # 路障
        for index in self.block_list:
            self.chess.set_value(index[0],index[1],self.GRID['RoadBlock'])
        # 终点
        self.chess.set_value(self.end_pos_x, self.end_pos_y, self.GRID['Destination'])

    def event_function(self,event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.exit()
            elif event.key == pygame.K_LEFT:
                self.go_left()
            elif event.key == pygame.K_RIGHT:
                self.go_right()
            elif event.key == pygame.K_UP:
                self.go_up()
            elif event.key == pygame.K_DOWN:
                self.go_down()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pass

class AutoMazeAI(MazeGame):
    def __init__(self, config_file_name):
        MazeGame.__init__(self, config_file_name)
        self.action_num = 4
        self.reward_list = []
        self.action_dict = {'left':'left','right':'right','up':'up','down':'down'}
        self.init_reward_list()
        self.num = 0

    def init_reward_list(self):
        self.list_width = self.chess.width()
        self.list_height = self.chess.height()
        for x in range(0, self.action_num*self.list_height*self.list_width):
            self.reward_list.append(0)

    def get_forward(self,state):
        base = (self.list_width * state[1] + state[0])
        return self.reward_list[base],self.reward_list[base*2],self.reward_list[base*3],self.reward_list[base*4]
    def update_forward(self,pos,reward,forward):
        self.reward_list[pos] = self.reward_list[pos] + reward + 0.1 * forward

    def set_forward(self,state,action,reward,forward):
        base = (self.list_width * state[1] + state[0])
        if action == self.action_dict['left']:
            self.update_forward(base,reward,forward)
        elif action == self.action_dict['right']:
            self.update_forward(base*2,reward,forward)
        elif action == self.action_dict['up']:
            self.update_forward(base*3,reward,forward)
        elif action == self.action_dict['down']:
            self.update_forward(base*4,reward,forward)
    def max_reward_action(self,list):
        max = 0
        for index in range(0,len(list)):
            if list[max] < list[index]:
                max = index
        if max == 0:
            return self.action_dict['left']
        elif max == 1:
            return self.action_dict['right']
        elif max == 2:
            return self.action_dict['up']
        elif max == 3:
            return self.action_dict['down']
    def max_reward(self,list):
        pos = 0
        max = list[pos]
        for index in range(0, len(list)):
            if list[pos] < list[index]:
                max = list[index]
                pos = index
        return max
    def event_function(self,event):
        pass
    def get_state(self):
        return self.pos_x,self.pos_y
    def get_action(self):
        return self.action_dict

    def get_reward(self,result):
        if result == self.STATE['Win']:
            return 50
        elif result == self.STATE['MoveSucc']:
            return 0
        elif result == self.STATE['MoveBolck']:
            return 0
        elif result == self.STATE['OutRange']:
            return 0
        else:
            return 0
    def outrange(self,result):
        if result == self.STATE['OutRange']:
            return True
        else:
            return False
    def exec_action(self,action):
        if action == self.action_dict['left']:
            return self.go_left()
        elif action == self.action_dict['right']:
            return self.go_right()
        elif action == self.action_dict['up']:
            return self.go_up()
        elif action == self.action_dict['down']:
            return self.go_down()
    def main_function(self):
        state = self.get_state()
        if self.num < 10000:
            action = random.randint(0,3)
            if action == 0:
                action = self.action_dict['left']
                result = self.go_left()
            elif action == 1:
                action = self.action_dict['right']
                result = self.go_right()
            elif action == 2:
                action = self.action_dict['up']
                result = self.go_up()
            elif action == 3:
                action = self.action_dict['down']
                result = self.go_down()
            self.num = self.num +1
            print(self.num)
        else:
            forward = self.get_forward(state)
            print("this",forward)
            action = self.max_reward_action(forward)
            result = self.exec_action(action)
        reward = self.get_reward(result)

        next_state = self.get_state()
        next_forward = self.get_forward(next_state)
        #print("next",next_forward)
        next_max_forward = self.max_reward(next_forward)

        if self.outrange(result) == True:
            #print("TRUE")
            next_max_forward = -10
        #print("next_max", next_max_forward)
        self.set_forward(state,action,reward,next_max_forward)
        #time.sleep(0.2)

a= AutoMazeAI('config.ini')
a.start()
