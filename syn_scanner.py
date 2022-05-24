from scapy.all import sr1,TCP,IP
import threading
import ipaddress
import time
import queue
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
HOST = "10.211.55.17"
TARGET = "10.211.55.0/24"
MAX_THREADS = 5 #最大线程数量
POOL = threading.Semaphore(value = MAX_THREADS)
UPHOSTS = queue.Queue()
L  = [20,21,22,23,80,443,231,254]

def save_log():
    fileName = "test.txt"
    try:
        with open(fileName,"w") as f:
            while not UPHOSTS.empty():
                u = UPHOSTS.get()
                print(u)
                ip = u[0] # 192.168.1.1
                port = ",".join(map(str,u[1])) # 21,22...
                msg = f'{ip}\n{port}'
                f.writelines(msg)
            f.close()
    except Exception as e:
        print(e)


def syn_scan(target_ip,portList=None):
    """syn扫描

    Args:
        target_ip (str): 目标ip
        portList (list, optional): 端口列表

    Returns:
        list: 端口开放列表
    """
    uphosts = []
    #全扫描
    if(portList is None):
        portList = list(range(0,255))
        
    for port in portList:
        ans = sr1(IP(dst=target_ip) / TCP(dport=port), timeout=1, verbose=0)
        if (ans is not None and int(ans[TCP].flags) == 18):
            uphosts.append(port)
            print(f"host up {target_ip}:{port}")
        else:
            print(f"host down {target_ip}:{port}")
    return uphosts

class mythread(threading.Thread):
    def __init__(self,*args):
        threading.Thread.__init__(self)
        self.ip = args[0]
        self.portList = args[1]
        self._stop_event = threading.Event()

    def run(self):
        self.result = syn_scan(self.ip,self.portList)
        UPHOSTS.put([self.ip,self.result])
        POOL.release()
      
    def stop(self):
        self._stop_event.set()
    
    def getresult(self):
        return self.result

def run(subnet,portList=None):
    #子网
    for ip in ipaddress.ip_network(subnet).hosts():
        print(f"ip {ip}")
        POOL.acquire()
        t = mythread(str(ip),portList)
        t.start()

if __name__ == "__main__":
    a = time.time()
    
    run(TARGET,L)
    save_log()
    b = time.time()
    print(f"time:{b-a}")