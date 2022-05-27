#生成配置json
import json
import os
CONFIG_PATH = "./xxx"
OUTPUT_PATH = "./xx/xxx"
TMPL = "xxx."
CONFIG_LIST = []
OSPATH = os.path.dirname(os.path.abspath(__file__))

def find_module_json(module_name):
    """寻找到对应module的默认参数配置文件

    Args:
        module_name (str): module名 不带.json

    Returns:
        dict: module的参数
    """
    data = None
    path = f"{OSPATH}/{CONFIG_PATH}/{TMPL}{module_name}.json"
    try:
        with open(path,"r") as f:
            data = f.read()
            f.close()
        data = json.loads(data)
    except Exception as e:
        print(e)
    finally:
        return data

def find_configheader_json(json_name="config"):
    data = None
    path = f"{OSPATH}/{CONFIG_PATH}/{TMPL}{json_name}.json"
    print(path)
    try:
        with open(path,"r") as f:
            data = f.read()
            f.close()
        data = json.loads(data)
    except Exception as e:
        print(e)
    finally:
        return data

def add_child(parentjson,childname,childjson):
    out_json = parentjson
    if childname not in parentjson.keys():
        out_json[childname] = {}
    out_json[childname].update(childjson)
    return out_json

def generate_config_json(config_list):
    output_json = {}
    
    for module in config_list:
        if (module == "config"):
            config_json = find_configheader_json()
            output_json.update(config_json)
        else:
            tempdict = find_module_json(module)
            module_dict = {module:tempdict}
            output_json=add_child(output_json,'modules',module_dict)
    
    return output_json

def output_to_jsonfile(filename,jsondata):
    
    path = f"{OSPATH}/{OUTPUT_PATH}/{filename}.json"
    try:
        with open(path,"w") as f:
            json.dump(jsondata,f)
            f.close()
    except Exception as e:
        print(e)
    
        

if __name__ == "__main__":
    CONFIG_LIST = ['config']
    a = generate_config_json(CONFIG_LIST)
    output_to_jsonfile("xx",a)