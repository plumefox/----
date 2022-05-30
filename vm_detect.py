#!/usr/bin/env python
import ctypes
import os
import sys

def is_user_root():
    try:
        return os.getuid() == 0
    except Exception as e:
        pass


def openvz_virtuozzo_detect():
     # check OpenVZ/Virtuozzo
    if os.path.exists("/proc/vz"):
        if not os.path.exists("/proc/bc"):
            print ("openvz container")
        else:
            print ("openvz node")
        return True
    return False

def xen_detect():
    # check Xen
    if os.path.exists("/proc/xen/capabilities"):
        if (os.path.getsize("/proc/xen/capabilities") > 0):
            print ("xen dom0")
        else:
            print ("xen domU")
        return True
    return False

def uml_detect():
    # check User Mode Linux (UML)
    try:
        with open("/proc/cpuinfo",'r') as f:
            buffer = f.read()
            f.close()
        if (buffer.find("UML") > 0):
            print ("uml")
            return True
    except Exception as e:
        # print(e)
        return False

def vm_detect():
    try:
        exec("virt-what")
        return True
    except Exception as e:
        print(e)
    return False
    

    

def linux_vm_detect():
    if (not is_user_root()):
        print("not root")
        sys.exit(0)
    
    if(openvz_virtuozzo_detect()):
        sys.exit(0)
    if(xen_detect()):
        sys.exit(0)
    if(uml_detect()):
        sys.exit(0)
    
    print("pass all vm test")
    

def run(**kwargs):
    if(os.name == "nt"):
        print("windows还没有制作")
        sys.exit(0)
    elif(os.name == "posix"):
        linux_vm_detect()
    else:
        print("Unknown system")
        sys.exit(0)
   
if __name__ == '__main__':
    # run()
    vm_detect()