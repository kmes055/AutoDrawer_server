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
        subprocess.Popen(command.split())
    elif model == 'DiscoGAN':
        if not os.path.exists(texture_path):
            return None
        command = disco_commands + id
        subprocess.Popen(command.split())


def color_split(colorString):
    cs = colorString[1:]
    r = int(cs[:2], 16)
    g = int(cs[2:4], 16)
    b = int(cs[4:], 16)
    return r, g, b


progress = 0.
def setProgress():
    global progress
    progress = 0.


def getProgress(token, category):
    out_category = 'shoes' if category == 'handbag' else 'handbag'
    global progress
    dir_name = 'C:/Capstone/server_dataset/%s/' % token
    if progress < .1:
        if os.path.exists(dir_name + 'sketch/%s.jpg' % category):
            progress += .1
        elif progress == .09:
            return progress
    elif progress < .5:
        if os.path.exists(dir_name + 'segmentation/%s.jpg' % category):
            progress += .4
        elif progress == .49:
            return progress
    elif progress < .8:
        if os.path.exists(dir_name + 'textureGAN/%s.jpg' % category):
            progress += .3
        elif progress == .79:
            return progress
    else:
        if os.path.exists(dir_name + 'discoGAN/%s.jpg' % out_category):
            progress = 1
        else:
            if progress >= 1:
                progress = 0.99
    if progress < 1 and int(progress*100) % 100 != 99:
        progress += .01
    return progress


'Thread part'

# def start_new_thread(function):
#     def decorator(*args, **kwargs):
#         t = Thread(target=function, args=args, kwargs=kwargs)
#         t.daemon = True
#         t.start()
#     return decorator
#
