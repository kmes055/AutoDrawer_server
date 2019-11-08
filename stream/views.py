from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.core.files.base import ContentFile

from .models import UserList, UploadModel, DownloadModel
from .forms import UploadForm, DownloadForm
from AI import functions
from station import settings

import json
from base64 import b64encode, b64decode
from PIL import Image


def __create_new_user(token):
    for i in range(settings.MAX_USER):
        try:
            UserList.objects.get(uid=i)
        except UserList.DoesNotExist:
            return UserList(pk=token, uid=i)


def cross(request, token):
    """
    Check request method type(GET, POST) and redirect request to proper stream.
    GET will be redirected to download to send transformed file
    POST will be redirected to upload to save transferred file
    :param request: request from client includes
    :param token: String. unique key per each user.
    :return: None
    """
    # TODO
    # 1. change token into user id
    # 2. Drop token column from request body.
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'GET':
        user_object = get_object_or_404(UserList, pk=token)
        uid = int('%s' % user_object)
        try:

            del data['token']
            data['uid'] = uid

            category = data['category']
            ext = functions.AI_ext

            filename = '%d_%s.%s' % (uid, category, ext)
            img = open(filename, 'r')

            # TODO
            # make response instance, Just body done.
            # Should divide non-critical part and make them out of this scope.
            return HttpResponse(data=img, content_type='image/jpg', category=category)
        except (KeyError, UserList.DoesNotExist):
            raise Http404('No user using this token %s' % token)
    elif request.method == 'POST':
        try:
            user_object = UserList.objects.get(pk=token)
        except UserList.DoesNotExist:
            user_object = __create_new_user(token)

        uid = int('%s' % user_object)

        sketch = data['sketch']
        pattern = data['pattern']
        category = data['category']
        use_recommend = data['use_recommendation']

        sketch_img = sketch['uri']

        if pattern['is_color']:
            color = functions.color_split(pattern['image_info'])
            pattern_img = Image.new('RGB', (32, 32), color)
        else:
            pattern_img = pattern['image_info']

        try:
            img = data['file'].split(';base64,')
            filename = lambda image: '%d.%s' % (uid, image['content_type'].split('/')[-1])

            form1 = UploadForm(uid, filename(sketch), img)
            form2 = UploadForm(uid, filename(pattern), img)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
                functions.file_transform(sketch_img, pattern_img, category, use_recommend)
                response = {'message': 'update done.', 'uid': uid}
                return HttpResponse(json.loads(response))
        except (KeyError, UserList.DoesNotExist):
            raise Http404('UserList does not exist')
        else:
            return Http404("Something's wrong.")


# def download(request, uid):
#     model = DownloadModel(uid=uid)
#     form = DownloadForm(request.POST, request.FILES, instance=model)
#
#     if form.is_valid():
#         pass
#     else:
#         raise Http404('Download form is not valid!!')
#
#
# def upload(request, uid):
#     model = UploadModel(uid=uid)
#     form = UploadForm(request.POST, request.FILES, instance=model)
#
#     if form.is_valid():
#         format, imgstr = form['file'].split(';base64,')
#         ext = format.split('/')[-1]
#         filename = '%d.%s' % (uid, ext)
#         data = ContentFile(b64decode(imgstr), name=filename)  # You can save this as file instance.
#         model.file.save(filename, data, save=True)


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

