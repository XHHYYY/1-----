from threading import Thread, Semaphore
from time import time, sleep

MAX_DELAY = 10
TIME_UNIT = 0.1

# global Source
# global customer_list
# global waiting_list
# global txt2file

class server(Thread):
    
    def __init__(self, max_delay, server_num) -> None:
        Thread.__init__(self)
        self.max_delay = max_delay
        self.server_num = server_num
        
    def run(self):
        global txt2file
        begin_time = time()
        while(time() - begin_time < self.max_delay):
            Source.acquire(timeout=MAX_DELAY)
            if waiting_list != []:
                customer = waiting_list[0]
                del(waiting_list[0])
                
                assert isinstance(customer, Customer)
                customer.service_begin_time = int((time() - begin_time) / TIME_UNIT)
                customer.server_num = self.server_num
                customer.leave_time = customer.service_begin_time + customer.required_time
                
                txt2cmd = '{0:^5} {1:^5} {2:^5} {3:^5} {4:^5} {5:^5}'.format( 
                      customer.num, customer.arrive_time, customer.required_time, 
                      customer.service_begin_time, customer.leave_time, customer.server_num)
                txt2file += txt2cmd + '\n'
                print(txt2cmd)
                
                sleep(customer.required_time * TIME_UNIT)
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
        sleep(TIME_UNIT / 2)
        if customer_list != []:
            if int((time() - begin_time) / TIME_UNIT) == customer_list[0].arrive_time:
                waiting_list.append(customer_list[0])
                del(customer_list[0])
                Source.release()
        # print('giver active\n')
        



if __name__ == '__main__':
    n = 1
    
    Source = Semaphore(0)
    customer_list= read_sequence()
    waiting_list = []
    head = '{0:^5} {1:^5} {2:^5} {3:^5} {4:^5} {5:^5}'.format('num', 'AT', 'RT', 'SBT', 'LT', 'SN')
    txt2file = head + '\n'
    
    print('{0:-^30}'.format('开始模拟'))
    print(head)
    
    thread_list = []
    for i in range(n):
        temp = server(MAX_DELAY, i+1)
        thread_list.append(temp)

    Top = Thread(target=list_ctrl)
    
    for i in range(n):
        thread_list[i].start()
    Top.start()
    
    Top.join()
    for i in range(n):
        thread_list[i].join()
    
    if waiting_list != []:
        raise Exception('模拟超时，请增加 MAX_DELAY 并重试')
    
    with open('./codes/results.txt', 'w') as f:
        f.write(txt2file)
    
    print('{0:-^30}'.format('模拟结束'))
