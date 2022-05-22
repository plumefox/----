import queue
import sys
import threading
import requests
import LucyGirlTrojan

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
THREADS = 50
EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
TARGET = "http://127.0.0.1:38769"



def build_wordlist(wordlist_file,resume = None):
    """爆破字典文件

    Args:
        wordlist_file (_type_): _description_
    """
    def extend_words(word):
        
        if "." in word:
            words.put(f'/{word}')
        else:
            # 目录
            words.put(f'/{word}/')

        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')
    
    try:
        words = queue.Queue()
        with open(wordlist_file,'r') as f:
            raw_words = f.read()
            f.close()
          
        # 断点续读jpg
        found_resume = False
        for word in raw_words.split():
            
            if(word[0] == "/"):
                word = word[1:]
                        
            if resume is not None:
                if found_resume:
                    extend_words(word)
                elif word == resume:
                    found_resume = True
                    print(f'Resuming wordlist from: {resume}')
            else:
                print(word)
                extend_words(word)

    except Exception as e:
        print(e)
    finally:
        return words

def dir_bruter(word_queue):
    headers = {'User-Agent':AGENT}
    
    while not word_queue.empty():
        url = f'{TARGET}{word_queue.get()}'
        try:
            r = requests.get(url,headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x')
            sys.stderr.flush()
            continue
        if r.status_code == 200:
            print(f'\nSuccess ({r.status_code}: {url})')
        elif r.status_code == 404:
            sys.stderr.write('.')
            sys.stderr.flush()
        else:
            print(f'{r.status_code} => {url}')


if __name__ == "__main__":
    words = build_wordlist("./sensitive.txt")
    print('Press return to continue.')
    sys.stdin.readline()
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start()
    
    
    

