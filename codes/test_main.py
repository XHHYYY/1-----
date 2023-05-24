from threading import Thread, Semaphore
from random import randint
from time import time, sleep

MAX_DELAY = 60
MODE = 1
temp = 0.5 / (MODE**3)
CHECK_PRECISION = temp # 0.5ms检查一次

class server(Thread):
    def __init__(self, max_delay, server_num) -> None:
        Thread.__init__(self)
        self.max_delay = max_delay
        self.server_num = server_num
        
    def run(self):
        begin_time = time()
        while(time() - begin_time < self.max_delay):
            print(self.server_num)
            sleep(CHECK_PRECISION / 5)
            Source.acquire(timeout=3)
            if waiting_list != []:
                customer = waiting_list[0]
                del(waiting_list[0])
                assert isinstance(customer, Customer)
                customer.service_begin_time = MODE * int(time() - begin_time)
                customer.server_num = self.server_num
                customer.leave_time = customer.service_begin_time + customer.required_time
                print('num:{0}, AT:{1}, RT:{2}, SBT:{3}, LT:{4}, SN:{5}'.format( 
                      customer.num, customer.arrive_time, customer.required_time, 
                      customer.service_begin_time, customer.leave_time, customer.server_num))
                sleep(customer.required_time / (MODE**3))
        return

class Customer():
    def __init__(self, num, arrive_time, required_time) -> None:
        self.num = num
        self.arrive_time = arrive_time
        self.required_time = required_time
        self.service_begin_time = None
        self.leave_time = None
        self.server_num = None

def read_sequence() -> list:
    with open('./codes/sequence.txt', 'r') as f:
        txt = f.read()
    customer_list = []
    list_sequence = txt.split('\n')
    for guy_info in list_sequence:
        if guy_info == '':
            break
        temp = list(map(int, guy_info.split()))
        customer_list.append(Customer(*temp))
    return customer_list

def list_ctrl():
    begin_time = time()
    while(time() - begin_time < MAX_DELAY):
        sleep(CHECK_PRECISION)
        if customer_list != []:
            if int(time() - begin_time) * MODE == customer_list[0].arrive_time:
                waiting_list.append(customer_list[0])
                del(customer_list[0])
                Source.release()
        # print('giver active\n')
        



if __name__ == '__main__':
    global Source
    global customer_list
    global waiting_list
    
    customer_list= read_sequence()
    Source = Semaphore(0)
    waiting_list = []
    
    
    
    p1  = server(MAX_DELAY, 1)
    p2  = server(MAX_DELAY, 2)
    p3  = server(MAX_DELAY, 3)
    Top = Thread(target=list_ctrl)
    
    p1.start()
    p2.start()
    p3.start()
    Top.start()
    
    Top.join()
    p3.join()
    p2.join()
    p1.join()
    
    print('main alive')