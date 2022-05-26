# python 模块导入

import base64
import importlib
#import imp #python 3.4弃用
import requests
import sys

class test:
    def __init__(self,name):
        self.name = name
    def module_runner(self,module):
        """运行module 每个module都要有run方法

        Args:
            module (_type_): _description_
        """
        result = sys.modules[module].run()
        print(result)
    def get_module(self,module):
        if module not in sys.modules:
            exec(f"import {module}")
    
    def run(self):
        self.get_module(self.name)
        self.module_runner(self.name)

class LuckyGirlImporter(object):
    def __init__(self) -> None:
        self.url = "http://10.211.55.17" #web url
        self.current_module_code = ""
        # self.res = self.__web_server_connect
    
    def __web_server_connect():
        """需要登录的情况,返回session

        Returns:
            _type_: _description_
        """
        sess = None
        return sess
    
    def __get_file_content(self,dir_name,module_name):
        """远程文件内容获取

        Args:
            url (_type_): _description_
            module_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        # http://xxx.com/xxx/xxx
        url = f"{self.url}/{dir_name}/{module_name}"
        r = requests.get(url=url)
        if (r.status_code == 200):
            return r.content
        return None
        
    
    def find_module(self,fullname,path=None):
        """查找器

        Args:
            fullname (_type_): _description_
            path (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        print(f"[ * ]Attemping to retrieve {fullname} ")
        new_library = self.__get_file_content("modules",f'{fullname}.py')
        if new_library is not None:
            # self.current_module_code = base64.b64decode(new_library)
            self.current_module_code = new_library.decode()
            return self
        return None
    
    def load_module(self,name):
        """导入器

        Args:
            name (_type_): _description_

        Returns:
            _type_: _description_
        """
        print(f"[ * ]Start install {name}")
        spec = importlib.util.spec_from_loader(name, loader=None,
                                               origin=self.url)
        new_module = importlib.util.module_from_spec(spec)
        exec (self.current_module_code,new_module.__dict__)
        sys.modules[spec.name] = new_module
        return new_module


def install_Importer():
    module_loader = LuckyGirlImporter()
    sys.meta_path.append(module_loader)

if __name__ == "__main__":
    install_Importer()
    t = test('hello')
    t.run()
    
    