# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 19:16:04 2019

@author: Sainath.Reddy
"""
import threading
import time

start = time.time()

cv1 = threading.Condition()
num=0
def first(cv1, th):
    global num
    flag=False
    while(num<10000):
        with cv1:
            num+=1
            print(f'{num} - {th}')
            cv1.notify_all()
            cv1.wait()

t1 = threading.Thread(target=first, args=(cv1, 't1'))
t2 = threading.Thread(target=first, args=(cv1, 't2'))
t1.start()
t2.start()
t1.join()
end = time.time()
time_taken = end - start
print('Time: ',time_taken)
