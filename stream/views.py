import json
import base64
import os
from PIL import Image

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from AI import functions, metadata


@csrf_exempt
def cross(request):
    """
    Check request method type(GET, POST) and redirect request to proper stream.
    GET will be redirected to download to send transformed file
    POST will be redirected to upload to save transferred file
    :param request: request from client includes
    :return: None
    """
    # TODO
    # 1. change token into user id
    # 2. Drop token column from request body.

    # data: Dictionary

    token = request.headers['token']
    ext = metadata.AI_ext
    if request.method == 'GET':
        """
        GET method must requested after transformation.
        Find result filenames, open image in server, send Image object.
        """
        base_path = 'C:/Capstone/server_dataset/'
        user_dir = base_path + token + '/'
        mode = request.headers['mode']
        category = request.headers['category']
        out_category = 'shoes' if category == 'handbag' else 'handbag'

        if mode == 'progress':
            progress = float(request.headers['progress'])
            progress = functions.getProgress(progress, token, category)
            data = {'progress': str(progress)}
            return HttpResponse(json.dumps(data))
        elif mode == 'result':
            with open(user_dir + 'TextureGAN/%s.jpg' % category, 'rb') as f:
                img1 = base64.b64encode(f.read())
            with open(user_dir + 'DiscoGAN/%s.jpg' % out_category, 'rb') as f:
                img2 = base64.b64encode(f.read())
            data = {'textureGAN': img1, 'discoGAN': img2}
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse('test')

    elif request.method == 'POST':
        """
        POST method must requested before transformation.
        Make save image path, create uid if new, image encoding format
        is discussing now.
        """
        data = json.loads(request.body.decode('utf-8'))

        if not metadata.exist(token):
            if metadata.push(token) == -1:
                return HttpResponse('Server is busy now. please reconnect just moment later.')

        mode = data['mode']
        category = data['category']

        if mode != 'upload':
            return HttpResponse('mode is not valid.')

        if category not in ['shoes', 'handbag']:
            return Http404('Category must be one of shoes or handbag')

        sketch = data['sketch']
        pattern = data['pattern']
        dir_root = os.path.join(metadata.dir_root, token + '/')
        filename = '%s.%s' % (category, ext)
        sketch_path = os.path.join(dir_root, 'sketch/', filename)
        pattern_path = os.path.join(dir_root, 'pattern/', filename)
        segment_path = os.path.join(dir_root, 'segmentation/', filename)

        with open(sketch_path, 'wb') as f:
            f.write(base64.decodebytes(str.encode(sketch)))

        if len(pattern) == 7:
            color = functions.color_split(pattern)
            pattern_img = Image.new('RGB', (64, 64), color)
            pattern_img.save(pattern_path)
        else:
            with open(pattern_path, 'wb') as f:
                f.write(base64.decodebytes(str.encode(pattern)))

        import subprocess
        command = 'C:/Capstone/Pytorch-TextureGAN/async.py %s %s' % (token, category)
        subprocess.call(command.split())

        return HttpResponse('ok')
        #
        # segmentate(sketch_path, segment_path)
        #
        # result = functions.file_transform(mode, token, category)
        # if not result:
        #     raise Http404('file transform error')
        #
        # # result = Image.open(result)
        # with open(result, 'rb') as f:
        #     result = base64.b64encode(f.read())
        #
        # response = {'message': 'update done.', 'result': result}
        # response = HttpResponse(data=json.dumps(response))
        # metadata.pop(token)
        #
        # return response


"""
Write json to file
"""
# with open('data.txt', 'w') as outfile:
#     json.dump(jsonData, outfile, sort_keys=True, indent=4,
#               ensure_ascii=False)

"""
Decode base64
"""
# import base64
#
# with open("yourfile.ext", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())

