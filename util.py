import platform
def get_path(path,flag=False):
    sys = platform.system()
    if sys == 'Windows':
        return path
    else:
        return path.replace('\\','/')