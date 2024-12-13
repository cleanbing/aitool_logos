'''
    Common utils library
'''

# -*- coding: utf-8 -*-

import sys as sys           # For stdout redirect to screen and files
import time as time         # For log filename auto-generation
import json as json         # For Json read/write
import re as re             # For regular search
from datetime import datetime # For date string format
import configparser
import msvcrt
import os

'''
    Global Definitions
'''


'''
Common Utilities
'''

def clear_subdirectories(directory):
    '''
        清空输入的目录下的所有子目录里面的文件
    '''
    # 遍历指定目录下的所有子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 构建文件的完整路径
            file_path = os.path.join(root, file)
            # 删除文件
            os.remove(file_path)
    print(f'>>> 已清空目录 {directory} 下的所有文件.')


def auto_create_folder(folder_path)->bool:
    '''
        自动创建目录, 若目录已存在返回False 否则返回True
    '''
    # 检查目录是否存在
    if not os.path.exists(folder_path):
        # 如果不存在，则创建目录
        os.makedirs(folder_path)
        print(f">>> 目录 {folder_path} 创建成功.")
        return True
    else:
        return False


def extract_text_and_img(html_content):
    '''
        提取p,h1,h2,h3,h4,h5,h6,img标签内容
    '''
    pattern = r'<p.*?>.*?</p>|<img .*?>|<h[1-6].*?>.*?</h[1-6]>'
    results = re.findall(pattern, html_content, re.DOTALL)
    lines = []
    for res in results:
        line = ''
        # 若为p或h标签则去掉标签中的其它类
        textMatch = re.match(r'<(p|h[1-6]).*?>(.*?)</\1>', res)
        if textMatch:
            # 去除空行
            if textMatch.group(2):
                line = f'<{textMatch.group(1)}>{textMatch.group(2)}</{textMatch.group(1)}>'
                lines.append(line)
            continue

        imgMatch = re.match(r'<img\s+src=\"(https:.*?)[?\"].*?>', res)
        if imgMatch:
            line = f'<p><img src="{imgMatch.group(1)}" width="100%"></p>'
            lines.append(line)
    return(''.join(lines))

def recursive_traverse(soup_object, indent=0):
    """
    递归遍历BeautifulSoup对象，打印每个标签和它的内容。
    :param soup_object: BeautifulSoup对象
    :param indent: 递归深度的缩进量
    """
    if isinstance(soup_object, str):
        return(soup_object)
    elif soup_object.name:
        print('  ' * indent, soup_object.name)
        for child in soup_object.children:
            s = recursive_traverse(child, indent + 1)
            if soup_object.name in ['p', 'b', 'i', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'img']:
                return()

            
def replace_fullwidth_punctuation(text):
    # 全角标点符号及其对应的半角标点符号
    fullwidth_punctuation = {
        '，': ',',  # 中文逗号
        '。': '.',  # 中文句号
        '！': '!',  # 中文感叹号
        '？': '?',  # 中文问号
        '：': ':',  # 中文冒号
        '；': ';',  # 中文分号
        '“': '"',  # 中文双引号开始
        '”': '"',  # 中文双引号结束
        '‘': "'",  # 中文单引号开始
        '’': "'",  # 中文单引号结束
        '（': '(',  # 中文左括号
        '）': ')',  # 中文右括号
        '【': '[',  # 中文左方括号
        '】': ']',  # 中文右方括号
        '《': '<',  # 中文书名号开始
        '》': '>',  # 中文书名号结束
        '、': ',',  # 中文顿号
        '—': '-',  # 中文破折号
        '～': '~',  # 中文波浪线
        '…': '...',  # 中文省略号
        '·': '.',  # 中文点号
        '—': '-',  # 中文破折号
        '——': '--',  # 中文长破折号
        '—': '-',  # 中文短破折号
        '—': '-',  # 中文连接号
        '—': '-',  # 中文间隔号
        '—': '-',  # 中文波浪线
        '—': '-',  # 中文下划线
        '—': '-',  # 中文上划线
        '—': '-',  # 中文着重号
        '—': '-',  # 中文专名号
        '—': '-',  # 中文间隔号
        '—': '-',  # 中文连接号
        '—': '-',  # 中文波浪线
        '—': '-',  # 中文下划线
        '—': '-',  # 中文上划线
        '—': '-',  # 中文着重号
        '—': '-',  # 中文专名号
    }

    # 构建替换模式
    pattern = '|'.join(re.escape(key) for key in fullwidth_punctuation.keys())

    # 替换全角标点符号
    def replace_match(match):
        return fullwidth_punctuation[match.group(0)]

    # 执行替换
    return re.sub(pattern, replace_match, text)

def generate_valid_filename(filename):
    '''
        生成合法的文件名: 全角替换为半角, 去除文件名中不允许的特殊字符
    '''
    # 替换文件名中的特殊字符
    filename = replace_fullwidth_punctuation(filename)
    filename = filename.replace('?', '')
    filename = filename.replace('<', '[')
    filename = filename.replace('>', ']')
    return filename

def save_as_html(title, body_content, filename):
    # 完整的HTML模板
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>{pageTitle}</title>
    </head>
    <body style="width: 60%; margin: 0 auto;">
        {bodyContent}
    </body>
    </html>
    """

    # 使用模板填充内容
    full_html_content = html_template.format(pageTitle=title, bodyContent=body_content)

    # 保存到文件
    print(f'>>> 文件成功保存: {filename}')
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(full_html_content)


def myExit(log):
    print('\n')
    print('='*100)
    print('>>> 知乎自动化工具运行结束!!!')
    print(f'>>> 若发现问题, 请联系开发者! (微信: cleanbing)')
    print('='*100)
    log.reset()
    print('>>> 请按任意键退出...\n\n')
    msvcrt.getch()
    exit()


def clear_txt_file(file_path):
    try:
        f = open(file_path, 'w', encoding='utf-8')
        f.close()
    except Exception as e:
        print(f"清空文件 {file_path} 时发生错误: {e}")
        raise

def load_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def append_txt_file(file_path:str, line:str):
    try:
        with open(file_path, 'a+', encoding='utf-8') as f:
            f.write(f"{line}\n")
            f.close()
    except Exception as e:
        print(f"写入文件 {file_path} 时发生错误: {e}")
        raise

def save_txt_file(file_path:str, lines:list):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
            f.close()
    except Exception as e:
        print(f"写入文件 {file_path} 时发生错误: {e}")
        raise    

'''
    返回今天的日期对应的字符串: 2024-07-25
'''
def get_today_str()->str:
    # 获取当前日期
    current_date = datetime.now()
    # 格式化日期为 'YYYY-MM-DD' 格式
    return(current_date.strftime('%Y-%m-%d'))

def load_ini_config():
    """
    加载并解析指定的INI文件
    """
    # 创建配置分析器对象
    config = configparser.ConfigParser()
    file_path = 'config.ini'

    # 使用指定的编码读取ini文件
    try:
        with open(file_path, 'r', encoding='UTF8') as file:
            config.read_file(file)
            return(config)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误: {e}")
    
    return None


def write_ini_config(config):
    try:
        with open('config.ini', 'w', encoding='UTF8') as file:
            config.write(file)
    except Exception as e:
        print(f"写入INI文件时发生错误: {e}")
        raise

def get_date_form_timestamp(timestamp):
    # 将时间戳转换为datetime对象
    dt_object = datetime.fromtimestamp(timestamp)
    # 将datetime对象转换为可读的时间格式
    time_str = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    date = extract_date_from_text(time_str)
    return date

def extract_date_from_text(text):
    if not text:
        return ''
    # 使用正则表达式匹配日期
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    dates = date_pattern.findall(text)
    if not dates or not len(dates): 
        return None
    else:
        return(dates[0])

def extract_link_from_text(text):
    if not text:
        return None
    # 使用正则表达式匹配URL
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = url_pattern.findall(text)
    if not urls or not len(urls): 
        return None
    else:
        return(re.sub(r'\?.*', '', urls[0]))

'''
    Save dict to txt file by json format
'''
def saveDictToJson(dict_content, save_file):
    with open(save_file, mode='w', encoding='utf-8') as output_file:
        json.dump(dict_content, output_file, ensure_ascii=False, indent=4)
    # print('Dict content has been saved to json: ', save_file)

'''
    Return {} if file not exist
'''
def loadJsonFromFile(json_file):
    try:
        with open(json_file, mode='r', encoding='utf-8') as file:
            return(json.load(file))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

'''
    Common Classes
'''

'''
    Logger to print log on screen and also saved to log file
'''
class Logger(object):
    logFile = ''
    def __init__(self, single_log_mode=False, default_log_file='log.txt'):
        self.terminal = sys.stdout
        sys.stdout = self
        if single_log_mode:
            self.logFile = default_log_file
        else:
            self.logFile =  f'./log/{time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())}.log'
        self.log = open(self.logFile, 'w', encoding="utf-8")
        print('>>> 已启动日志文件：', self.logFile)
 
    def write(self, message):
        '''print equal to sys.stdout.write'''
        self.terminal.write(message)
        self.log.write(message)
 
    def reset(self):
        print('>>> 所有日志已保存')
        self.log.close()
        sys.stdout=self.terminal
    
    def flush(self):
        pass



