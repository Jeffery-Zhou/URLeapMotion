# -*- coding: UTF-8 -*-
import threading, time

def fun1():
    while True:
        time.sleep(2)
        print("fun1")

def fun2():
    while True:
        time.sleep(6)
        print("fun2")

threads = []
threads.append(threading.Thread(target=fun1))
threads.append(threading.Thread(target=fun2))
print(threads)
if __name__ == '__main__':
    for t in threads:
        print(t)
        t.start()