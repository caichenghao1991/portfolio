import getpass
import logging
import os
import platform
import shutil
import stat
import subprocess
import zipfile
from pathlib import Path

from util import get_path

logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')


def cmd_execute(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    ex.wait()
    return out.decode()


def set_kaggle_token():
    sys = platform.system()
    cur = os.getcwd() + get_path('\\kaggle.json')
    if sys == 'Windows':
        path = f'C:\\Users\\{getpass.getuser()}\\.kaggle\\kaggle.json'
        new_dir = '\\'.join(path.split('\\')[:-1])
        if not Path(new_dir).exists():
            os.mkdir(new_dir)
        if not Path(path).exists():
            shutil.copy(cur, new_dir)
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 777
    else:
        path = '~/.kaggle/kaggle.json'
        new_dir = '/'.join(path.split('/')[:-1])
        if not Path(new_dir).exists():
            os.mkdir(new_dir)
        if not Path(path).exists():
            shutil.copy(cur, new_dir)
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    print(path)


def unzip(count, path=get_path(f'{os.getcwd()}\\static\\data'),flag=True):
    files = []
    suffix = ['rar', 'zip', '7z']
    lists = os.listdir(path)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(path + get_path("\\") + fn), reverse=True)  # 按时间排序
    res = [x for x in lists[:count] if str(x).split('.')[-1] in suffix]

    for file in res:
        if '.zip' in file:
            logging.warning(f'{file} unzipped!')
            folder_name = get_path(f'{path}\\{"".join(file.split(".")[:-1])}')
            if not Path(folder_name).exists():
                os.mkdir(folder_name)
            file_path = get_path(f'{path}\\{file}')
            zip_file = zipfile.ZipFile(file_path, 'r')
            for filename in zip_file.namelist():
                zip_file.extract(filename, folder_name)
            zip_file.close()
            files.append(file)
            if flag:
                os.remove(file_path)
    return files

def grab_search_result(topic, count=1):
    cmd = cmd_execute(f'kaggle datasets list -s {topic}')
    lines = cmd.split('\n')  # 读文件kaggle datasets list -s {topic}
    column_name = list(filter(lambda x: x is not '', [x for x in lines[0].split('  ')]))
    file_list = [list(filter(lambda x: x is not '', [x for x in lines[i].split('  ')])) for i in range(2, len(lines))]

    data = []
    for i in range(len(file_list) - 1):
        row = {}
        for j in range(len(column_name)):
            row.update({column_name[j]: file_list[i][j]})
        data.append(row)

    for i in range(count):
        cmd_execute(f'kaggle datasets download {data[i]["ref"]} -p ./static/data')


def retrieve_csv(subject, count):
    if type(count) is type(1) and int(count) < 20:
        grab_search_result(subject, count)
        files = unzip(count)
        logging.warning('all files downloaded and unzipped!')
    return files
if __name__ == '__main__':  # Runs main() if file wasn't imported.kaggle datasets list - s iris
    retrieve_csv('iris', 3)
