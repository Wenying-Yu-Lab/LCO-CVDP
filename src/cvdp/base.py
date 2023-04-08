import os
import sys
import csv
from typing import List, Dict, Callable
import chardet
from copy import deepcopy


# 自动检测文件编码
def auto_enco(fn: str) -> str:
    with open(fn,'rb') as f:
        text = f.read()
        res = chardet.detect(text)
    return res['encoding']

# 将路径中的反斜杠替换并删除末尾斜杠
def refine_path(path: str) -> str:
    if path == '' or path is None:
        return ''
    res = path.replace('\\','/')
    if res[-1] == '/' and res != '/':
        res = res[:-1]
    return res
