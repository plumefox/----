# -*- coding: utf-8 -*-
# ***   author:LC   ***
# created date：2022/5/17
# description：Doraemon

def shell_import(shell_dir):
    """导入shell文件到工具内

    Args:
        shell_dir (str): shell文件的地址

    Returns:
        _tools_dir: tool内部的地址
    """
    _tools_dir = None
    
    try:
        with open(shell_dir,"r") as f:
            f.read()
    except:
        pass
    
    return _tools_dir


