import json
import base64
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
    data = json.loads(request.body.decode('utf-8'))
    token = json.loads(request.headers.decode('utf-8'))['token']

    if request.method == 'GET':
        """
        GET method must requested after transformation.
        Find result filenames, open image in server, send Image object.
        """
        if metadata.exist(token):
            uid = token[:6]
        else:
            raise Http404('No user using this token %s' % token)

        category = data['category']
        ext = metadata.AI_ext

        filename = '%d_%s.%s' % (uid, category, ext)
        img = open(filename, 'r')
        if img:
            return HttpResponse(data=img, content_type='image/jpg', category=category)
        else:
            return HttpResponse('Wait')

    elif request.method == 'POST':
        """
        POST method must requested before transformation.
        Make save image path, create uid if new, image encoding format
        is discussing now.
        """
        if not metadata.exist(token):
            metadata.push(token)

        uid = token[:6]

        sketch = data['sketch']
        pattern = data['pattern']
        category = data['category']
        recommend = data['recommend']

        ext = metadata.AI_ext

        sketch_path = '%s%s_%s.%s' % (metadata.sketch_dir, uid, category, ext)
        pattern_path = '%s%s_%s.%s' % (metadata.pattern_dir, uid, category, ext)

        with open(sketch_path, 'wb') as f:
            f.write(base64.decodebytes(str.encode(sketch)))

        if len(pattern) == 7:
            color = functions.color_split(pattern['image_info'])
            pattern_img = Image.new('RGB', (32, 32), color)
            pattern_img.save(pattern_path)
        else:
            with open(pattern_path, 'wb') as f:
                f.write(base64.decodebytes(str.encode(pattern)))

        # TODO
        # connect with forms, AI part.....
        # Think about multithreading(for GPU) / progressbar
        result = functions.file_transform(sketch_path, pattern_path, category, recommend)
        response = {'message': 'update done.', 'result': result}
        return HttpResponse(data=json.dumps(response))


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

