from threading import Thread, Lock
from subprocess import run

# Metadata

AI_ext = 'jpg'
file_transform_mutex = Lock()
category_list = ['handbag', 'shoes', 'hat']


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


@start_new_thread
def file_transform(sketch, pattern, category, use_recommend):

    # f = open(filename, 'r')
    # if category not in category_list:
    #     print('Wrong!!!')
    #     return None
    # if use_recommend:
    #     pass

    try:
        file_transform_mutex.acquire()
        """
        Do Something
        """

        params = {"TextureGAN": [],
                  "CycleGAN": []}  # AI parameters.
        # run('python')
        pass
    finally:
        file_transform_mutex.release()
        return sketch


def __transform_textureGAN(sketch, pattern, category, params):
    pass


def __transform_DiscoGAN(image, category, params):
    pass


def color_split(colorString):
    return (int(colorString[i:i+2]) for i in range(0, len(colorString), 2))
