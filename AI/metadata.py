from threading import Lock

max_user = 15
AI_ext = 'jpg'
file_transform_mutex = Lock()
category_list = ['handbag', 'shoes', 'hat']
sketch_dir = 'C:/Capstone/server_dataset/sketch/'
pattern_dir = 'C:/Capstone/server_dataset/pattern/'
__valid_tokens = []


def push(token):
    if len(__valid_tokens) == max_user:
        __valid_tokens.pop(0)
    __valid_tokens.append(token)
    return token


def pop(token):
    __valid_tokens.remove(token)


def exist(token):
    return token in __valid_tokens
