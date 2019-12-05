import subprocess
import os
from .metadata import dir_root

seg_commands = '''python C:/Capstone/Pytorch-TextureGAN/segmentation.py'''
txt_commands = '''python C:/Capstone/Pytorch-TextureGAN/test.py 
--gpu 1 --model texturegan --batch_size 1 
--data_path C:/Capstone/server_dataset/ --num_input_texture_patch 1 
--num_local_texture_patch 1'''
disco_commands = '''python C:/Capstone/Pytorch_DiscoGAN/discogan_final.py 
--load_epoch -1 --batchSize 1 --data_root C:/Capstone/server_dataset/
'''


def file_transform(token, category):
    id = ' --token %s --category %s' % (token, category)

    command = seg_commands + id
    subprocess.Popen(command.split())
    command = txt_commands + id
    subprocess.Popen(command.split())
    command = disco_commands + id
    subprocess.Popen(command.split())
