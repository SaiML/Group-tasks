# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 12:07:10 2019

@author: Sainath.Reddy
"""

def decor(n):
    def wrap_1(func):
        def wrap_2(*args, **kwargs):
            for i in range(n):
                func(*args, **kwargs)
        return wrap_2
    return wrap_1

@decor(3)
def display(name):
    print(f'{name} is done with last task')
    
display('team')