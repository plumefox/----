# -*- coding: utf-8 -*-
# ***   author:LC   ***
# created date：2022/3/28
# description：网络工具的控制端=w= 
import sys
import getopt

# Extensions
import uclient
# 后面如果要带参数需要加冒号
opt_list = ["help","listen","execute","target","port","command","upload","debug"]
short_opts = "hle:t:p:cu:"

def usage():
    print("NET工具盒子=w=:")
    print("version:{0} updated data:{1}".format(uclient._version,uclient._updateDate))
    print("使用说明:")
    print("-h --help - 帮助信息喵")
    print("-l --listen - listen on[host]:[port]")
    print("-e --execute")
    print("-c --commandshell")
    print("-u --upload")

def panel():
    if not len(sys.argv[1:]):
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:],short_opts,opt_list)
        print(opts,args)
    except getopt.GetoptError as err:
        print (str(err))
        usage()
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
            sys.exit()
        elif o in ("-l","--listen"):
            uclient.Listen = True
        elif o in ("-e","--execute"):
            uclient.execute = a
        elif o in ("-c","--commandshell"):
            uclient.command = True
        elif o in ("-u","--upload"):
            uclient.upload_destination = a
        elif o in ("-t","--target"):
            uclient.target = a
        elif o in ("-p","--port"):
            uclient.port = int(a)
        elif o in ("--debug"):
            uclient._debugModel = True
        else:
            assert False,"unhandled option"
    uclient._debug_status("main")
    #openShell()
panel()

 
