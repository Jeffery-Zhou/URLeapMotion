import threading
from threading import Thread
from time import sleep
from random import randint
import time

class test():
    @staticmethod
    def print1():
        time.sleep(5)
        print("this message is from print1 ")

    @staticmethod
    def print2():
        print("this message is from print2 ")
        
    



def display(name, count):
	if count > 1:
		print "Now, %s has %d apples.\n" % (name, count),
	elif count == 1:
		print "Now, %s has  an apple.\n" % name,
	else:
		print "Now, %s has not any apples.\n" % name,
                
def eat_apple(name, count):
	display(name, count)
	while count > 0:
		print "%s eats an apple.\n" % name,
		count -= 1
		display(name, count)
		sleep(randint(1, 3))

class MyThread(Thread):
	"""docstring for MyThread"""
	def __init__(self, name, count):
		super(MyThread, self).__init__()
		self.name = name
		self.count = count

	def run(self):
            if self.count == 1:
                # pass
                test.print1(1)
            else:
                # pass
                test.print2(2)

# huey = MyThread("Huey", 1)
# sugar = MyThread("Sugar", 5)
# huey.start()
# sugar.start()

threads = []
threads.append(threading.Thread(target=test.print1, args=()))
threads.append(threading.Thread(target=test.print2, args=()))
for t in threads:
    t.start()


