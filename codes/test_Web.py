import time
from threading import Thread, Semaphore
lock_1 = Semaphore(1)     #检查售票员是否关门
lock_2 = Semaphore(0)     #检查司机是否停车
def Driver():
    for i in range(3):
 
            lock_1.acquire()
            print('司机开车')
            time.sleep(1)
            print('驾驶')
            print('到站停车')
 
            lock_2.release()
def Server():
    for i in range(3):
 
            lock_2.acquire()
            time.sleep(1)
            print('打开车门')
            print('乘客上下车')
            time.sleep(1)
            print('关上车门')
 
            lock_1.release()
if __name__=='__main__':
    p1 = Thread(target=Driver)
    p2 = Thread(target=Server)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
