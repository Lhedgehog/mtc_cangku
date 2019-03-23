import sys
import numpy as np
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Cargo_state(object):
    """
    cargo class for env
    """
    def __init__(self):
        super(Cargo_state,self).__init__()
        self.__cargo_num = 1

    def get_cargo_num(self):
        return self.__cargo_num

    def out_cargo(self):
        if self.__cargo_num == 0:
            print("no cargo, cant give cargo, Invalid operation..")
            raise ValueError
        else:
            self.__cargo_num = self.__cargo_num - 1

    def reset_cargo_num(self):
        self.__cargo_num = 1


# a = Cargo()
# # print(a.__cargo_num)
# print(a.get_cargo_num())
# a.out_cargo()
# a.__cargo_num = 2
# print(a.get_cargo_num())