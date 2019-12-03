import json
import base64
import os
from PIL import Image
from io import BytesIO

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from AI import functions, metadata
from AI.segmentation import segmentate

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

    if request.method == 'GET':
        """
        GET method must requested after transformation.
        Find result filenames, open image in server, send Image object.
        """
        
        # if metadata.exist(token):
        #     uid = token[:6]
        # else:
        #     raise Http404('No user using this token %s' % token)
        # 
        # category = data['category']
        # ext = metadata.AI_ext
        # 
        # filename = '%d_%s.%s' % (uid, category, ext)
        # img = open(filename, 'r')
        # if img:
        #     return HttpResponse(data=img, content_type='image/jpg', category=category)
        # else:
        #     return HttpResponse('Wait')
        return HttpResponse('test page')

    elif request.method == 'POST':
        """
        POST method must requested before transformation.
        Make save image path, create uid if new, image encoding format
        is discussing now.
        """
        data = json.loads(request.body.decode('utf-8'))
        token = request.headers['token']
        if not metadata.exist(token):
            if metadata.push(token) == -1:
                msg = 'Server is busy now. please reconnect a moment later.'
                print(msg)
                raise Http404(msg)
        mode = data['mode']
        category = data['category']
        if category not in ['shoes', 'handbag']:
            msg = 'Category must be one of shoes or handbag'
            print(msg)
            raise Http404(msg)
        ext = metadata.AI_ext
        if mode:
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
            segmentate(sketch_path, segment_path)

        model = 'TextureGAN' if mode else 'DiscoGAN'
        result = functions.file_transform(model, token, category)
        if not result:
            raise Http404('file transform error')

        result = Image.open(result)
        buffer = BytesIO()
        result.save(buffer)
        result = base64.b64encode(buffer.getvalue())
        
        response = {'message': 'update done.', 'result': result}
        response = HttpResponse(data=json.dumps(response))
        metadata.pop(token)
        
        return response


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

