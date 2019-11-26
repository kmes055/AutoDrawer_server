from threading import Thread
from .metadata import file_transform_mutex
from subprocess import run


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


# @start_new_thread
def file_transform(sketch, pattern, category, recommend):

    # f = open(filename, 'r')
    # if category not in category_list:
    #     print('Wrong!!!')
    #     return None
    # if use_recommend:
    #     pass

    try:
        # file_transform_mutex.acquire()
        """
        Do Something
        """

        params = {"TextureGAN": [],
                  "DiscoGAN": []}  # AI parameters.
        # run('python')
        pass
    finally:
        # file_transform_mutex.release()
        return sketch


def __transform_textureGAN(sketch, pattern, category, params):
    pass


def __transform_DiscoGAN(image, category, params):
    pass


def color_split(colorString):
    return (int(colorString[i:i+2]) for i in range(0, len(colorString), 2))
