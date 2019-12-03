from threading import Thread
import subprocess
import os
from .metadata import dir_root

txt_commands = '''python C:/Capstone/Pytorch-TextureGAN/test.py 
--gpu 1 --model texturegan --batch_size 1 
--data_path C:/Capstone/server_dataset/ --num_input_texture_patch 1 
--num_local_texture_patch 1'''
disco_commands = '''python C:/Capstone/Pytorch_DiscoGAN/discogan_final.py 
--load_epoch -1 --batchSize 1 --data_root C:/Capstone/server_dataset/
'''


def file_transform(model, token, category):
    id = ' --token %s --category %s' % (token, category)

    token_dir = os.path.join(dir_root, token + '/')
    texture_path = os.path.join(token_dir, 'textureGAN/', '%s.jpg' % category)

    if model == 'TextureGAN':
        command = txt_commands + id
        res = subprocess.check_call(command.split())
        if res != 0:
            print('subprocess1 error')
            return None
        return texture_path
    elif model == 'DiscoGAN':
        if not os.path.exists(texture_path):
            return None
        command = disco_commands + id
        res = subprocess.check_call(command.split())
        if res != 0:
            print('subprocess2 error')
            return None
        out_category = 'shoes' if category == 'handbag' else 'handbag'
        return os.path.join(token_dir, 'discoGAN/', '%s.jpg' % out_category)
    else:
        return None


def color_split(colorString):
    cs = colorString[1:]
    r = int(cs[:2], 16)
    g = int(cs[2:4], 16)
    b = int(cs[4:], 16)
    return r, g, b



'Thread part'

# def start_new_thread(function):
#     def decorator(*args, **kwargs):
#         t = Thread(target=function, args=args, kwargs=kwargs)
#         t.daemon = True
#         t.start()
#     return decorator
#
