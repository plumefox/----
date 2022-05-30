import ctypes
import platform
#关于python调用c语言dll
# ctypes.windll. dll名 . 函数名 

def messageboxdll():
    user32 = ctypes.windll.LoadLibrary('user32.dll')
    # ctypes.windll.user32.MessageBoxA(0, 'good', 'Ctypes', 0)
    user32.MessageBoxA(0, b"good ctypes", b'Ctypes', 0)

def cprintf():
    if platform.system() == 'Windows':
        libc = ctypes.cdll.LoadLibrary('msvcrt.dll')
    elif platform.system() =='Linux':
        libc = ctypes.cdll.LoadLibrary('libc.so.6')
    
    # msg = ctypes.c_wchar_p("hello ctypes \n")
    msg = b"hello ctypes"
    libc.printf(msg)


if __name__ == '__main__':
    messageboxdll()