import time
from threading import Thread, Semaphore
lock_1 = Semaphore(1)     #�����ƱԱ�Ƿ����
lock_2 = Semaphore(0)     #���˾���Ƿ�ͣ��
def Driver():
    for i in range(3):
 
            lock_1.acquire()
            print('˾������')
            time.sleep(1)
            print('��ʻ')
            print('��վͣ��')
 
            lock_2.release()
def Server():
    for i in range(3):
 
            lock_2.acquire()
            time.sleep(1)
            print('�򿪳���')
            print('�˿����³�')
            time.sleep(1)
            print('���ϳ���')
 
            lock_1.release()
if __name__=='__main__':
    p1 = Thread(target=Driver)
    p2 = Thread(target=Server)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
