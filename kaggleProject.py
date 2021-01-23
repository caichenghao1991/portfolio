import getpass
import logging
import os
import platform
import shutil
import stat
import subprocess
import zipfile
import kaggle

logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')


def cmd_execute(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    ex.wait()
    return out.decode()


def set_kaggle_token():
    sys = platform.system()
    cur = os.getcwd().replace("\\", '/') + '/kaggle.json'
    if sys == 'Windows':
        path = 'C:/Users/' + getpass.getuser() + '/.kaggle/kaggle.json'
        new_dir = '/'.join(path.split('/')[:-1])
    else:
        path = f'/home/{getpass.getuser()}/.kaggle/kaggle.json'
        new_dir = '/'.join(path.split('/')[:-1])

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    if not os.path.exists(path):
        shutil.copy(cur, new_dir)
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)  # 600
    print(path)


def unzip(count, path=os.getcwd().replace("\\", '/') + '/static/data', flag=True):
    files = []
    suffix = ['rar', 'zip', '7z']
    lists = os.listdir(path)  # 
    lists.sort(key=lambda fn: os.path.getmtime(path + '/' + fn), reverse=True)  # sort by time modified
    res = [x for x in lists[:count] if str(x).split('.')[-1] in suffix]

    for file in res:
        if '.zip' in file:
            logging.warning(f'{file} unzipped!')
            folder_name = f'{path}/{"".join(file.split(".")[:-1])}'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
            file_path = f'{path}/{file}'
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
    # cmd = os.popen(f'kaggle datasets list -s {topic}')
    lines = cmd.split('\n')  # kaggle datasets list -s {topic}
    column_name = list(filter(lambda x: x != '', [x for x in lines[0].split('  ')]))
    file_list = [list(filter(lambda x: x != '', [x for x in lines[i].split('  ')])) for i in range(2, len(lines))]

    data = []
    for i in range(len(file_list) - 1):
        row = {}
        for j in range(len(column_name)):
            row.update({column_name[j]: file_list[i][j]})
        data.append(row)

    for i in range(count):
        cmd_execute(f'kaggle datasets download {data[i]["ref"]} -p ./static/data')


def retrieve_csv(subject, count):
    files = []
    if isinstance(count, int) and int(count) < 20:
        set_kaggle_token()
        grab_search_result(subject, count)
        files = unzip(count)
        logging.warning('all files downloaded and unzipped!')
    return files


if __name__ == '__main__':  # Runs main() if file wasn't imported.kaggle datasets list - s iris
    retrieve_csv('iris', 3)
