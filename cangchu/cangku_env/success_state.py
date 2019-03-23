import sys
import numpy as np
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Sucess_state(object):
    """
    cargo class for env
    """
    def __init__(self):
        super(Sucess_state,self).__init__()
        self.__sucess = False
        self.__condition = 0

    def add_condition(self):
        self.__condition = self.__condition + 1

    def whether_sucess(self):
        if self.__condition == 2:
            self.__sucess = True
        else:
            self.__sucess = False
        return self.__sucess

    def reset_sucesss_state(self):
        self.__if_sucess = False
        self.__condition = 0

