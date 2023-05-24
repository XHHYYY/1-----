from threading import Thread, Semaphore
from random import randint
from time import time, sleep

MAX_DELAY = 5
def giver():
    global cur_source
    global Source_list
    begin_time = time()
    while(time() - begin_time < MAX_DELAY):
        sleep(1)
        cur_source.append(Source_list[0])
        del(Source_list[0])
        Source.release()
        print('giver alive\n')

def T1():
    begin_time = time()
    while(time() - begin_time < MAX_DELAY):
        Source.acquire(timeout=3)
        if cur_source != []:
            print(cur_source, 'printed by T1, time = {}'.format(time()-begin_time))
            del(cur_source[0])
        print('T1 alive')
    print('T1 alive')
    return

    
def T2():
    begin_time = time()
    while(time() - begin_time < MAX_DELAY):
        Source.acquire(timeout=3)
        if cur_source != []:
            print(cur_source, 'printed by T2, time = {}'.format(time()-begin_time))
            del(cur_source[0])
        print('T2 alive')
    print('T2 alive')
    return



if __name__ == '__main__':
    Source = Semaphore(0)
    Source_list = []

    for i in range(20):
        Source_list.append(randint(0, 100))

    cur_source = []
    
    p1 = Thread(target=T1)
    p2 = Thread(target=T2)
    Top = Thread(target=giver)
    
    p1.start()
    p2.start()
    Top.start()
    
    Top.join()
    p2.join()
    p1.join()
    
    print('main alive')