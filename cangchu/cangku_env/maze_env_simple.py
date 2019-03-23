"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
import numpy as np
import time
import sys
from cangku_env.cargo_state import Cargo_state
from cangku_env.success_state import Sucess_state
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


UNIT = 40   # pixels
MAZE_H = 5 # grid height
MAZE_W = 5 # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()
        self.cargo1_state = Cargo_state()
        self.cargo2_state = Cargo_state()
        self.sucess_state = Sucess_state()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([20, 20])

        # hell
        # i = range(2,9)
        # j = range(11,18)
        block0 = [1,3]
        block1 = [1]

        self.hell_horizontal = []
        for i in block0:
            for j in block1:
                hell_0_center = origin + np.array([UNIT*i,UNIT*j])
                hell_tem = self.canvas.create_rectangle(
                    hell_0_center[0] - 15, hell_0_center[1] - 15,
                    hell_0_center[0] + 15, hell_0_center[1] + 15,
                    fill='black')
                self.hell_horizontal.append(hell_tem)

        # i = range(3,8)
        # j = range(12,17)
        block0 = [1,3]
        block1 = [3]
        self.hell_vertical = []
        for i in block0:
            for j in block1:
                hell_0_center = origin + np.array([UNIT * i, UNIT * j])
                hell_tem = self.canvas.create_rectangle(
                    hell_0_center[0] - 15, hell_0_center[1] - 15,
                    hell_0_center[0] + 15, hell_0_center[1] + 15,
                    fill='black')
                self.hell_vertical.append(hell_tem)

        self.hell_list = self.hell_horizontal + self.hell_vertical
        self.hell_coor_list = []
        for hell in self.hell_list:
            self.hell_coor_list.append(self.canvas.coords(hell))


        # create oval
        oval_center = origin + UNIT * 4
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        #create cargo
        cargo_center1 = origin + np.array([UNIT * 1, UNIT * 2])
        self.cargo1 = self.canvas.create_rectangle(
            cargo_center1[0]-15,cargo_center1[1]-15,
            cargo_center1[0]+15,cargo_center1[1]+15,
            fill = 'yellow')
        cargo_center2 = origin + np.array([UNIT * 3, UNIT * 2])
        self.cargo2 = self.canvas.create_rectangle(
            cargo_center2[0] - 15, cargo_center2[1] - 15,
            cargo_center2[0] + 15, cargo_center2[1] + 15,
            fill='yellow')
        self.cargo_coor_list = []
        self.cargo_coor_list.append(self.canvas.coords(self.cargo1))
        self.cargo_coor_list.append(self.canvas.coords(self.cargo2))

        # pack all
        self.canvas.pack()


    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # reset cargo state
        self.cargo1_state.reset_cargo_num()
        self.cargo2_state.reset_cargo_num()
        self.sucess_state.reset_sucesss_state()
        # return observation
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # leftc
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.rect)  # next state

        # reward function
        if s_ == self.canvas.coords(self.oval):
            if self.sucess_state.whether_sucess() == True:
                reward = 2
                done = True
                s_ = 'terminal_oval'
                self.reset()
            else:
                reward = 0.5
                done = True
                s_ = 'terminal_oval'
                self.reset()
        elif s_ in self.hell_coor_list or s_ == s: #collision
            reward = -2
            done = True
            s_ = 'terminal_hell_or_bound'
            self.reset()
        elif s_ in self.cargo_coor_list:
            if s_ == self.cargo_coor_list[0]:
                if self.cargo1_state.get_cargo_num() == 0:
                    reward = -0.5
                else:
                    self.cargo1_state.out_cargo()
                    self.sucess_state.add_condition()
                    reward = 0.5
            else:
                if self.cargo2_state.get_cargo_num() == 0:
                    reward = -0.5
                else:
                    self.cargo2_state.out_cargo()
                    self.sucess_state.add_condition()
                    reward = 0.5
            done = False
        else:
            reward = -0.5
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.05)
        self.update()


