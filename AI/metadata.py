from threading import Lock
import os

max_user = 1
AI_ext = 'jpg'
file_transform_mutex = Lock()
category_list = ['handbag', 'shoes', 'hat']
dir_root = 'C:/Capstone/server_dataset/'

__valid_tokens = []


def push(token):
    if len(__valid_tokens) == max_user:
        return -1
    __valid_tokens.append(token)
    if not os.path.exists(dir_root + token):
        os.mkdir(dir_root + token)
        user_dir = dir_root + token + '/'
        os.mkdir(user_dir + 'sketch')
        os.mkdir(user_dir + 'segmentation')
        os.mkdir(user_dir + 'pattern')
        os.mkdir(user_dir + 'textureGAN')
        os.mkdir(user_dir + 'discoGAN')
    return token


def pop(token):
    __valid_tokens.remove(token)
    import shutil
    shutil.rmtree(dir_root + token)


def exist(token):
    return token in __valid_tokens
