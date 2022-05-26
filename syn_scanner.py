from scapy.all import sr1,TCP,IP
import ipaddress
import time
import logging
import multiprocessing 
import os
HOST = "10.211.55.17"
TARGET = "10.211.55.0/27"
MAX_THREADS = 32 #最大线程数量
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


L  = [20,21,22,23,80,443,231,254,65534]

def save_log(result,fileName):
    try:
        with open(fileName,"w") as f:
            for r in result:
                msg = ""
                u = r.get()
                ip = u[0] # 192.168.1.1
                if(u[1] == []):
                    continue
                port = ",".join(map(str,u[1])) # 21,22...
                msg = f'{ip}\t{port}\n'
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
    # print(f"process:{os.getgid()} {multiprocessing.current_process()}")
    uphosts = []
    #全扫描
    if(portList is None):
        portList = list(range(0,65535))
        
    for port in portList:
        ans = sr1(IP(dst=target_ip) / TCP(dport=port), timeout=1, verbose=0)
        if (ans is not None and int(ans[TCP].flags) == 18):
            uphosts.append(port)
            print(f"host up {target_ip}:{port}")
        else:
            pass
    # result_queue.put([target_ip,uphosts])
    return [target_ip,uphosts]



if __name__ == "__main__":
    a = time.time()
    fileName = f"{int(a)}.txt"
    result_list = []
    # UPHOSTS = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(MAX_THREADS)
    print(f"Start Process...")
    addrcount = ipaddress.ip_network(TARGET).num_addresses
    #子网
    for ip in ipaddress.ip_network(TARGET).hosts():
        result_list.append(pool.apply_async(syn_scan,args=(str(ip),L)))
    
    pool.close()
    pool.join()
    save_log(result_list,fileName)
    
    b = time.time()
    print(f"time:{b-a}")