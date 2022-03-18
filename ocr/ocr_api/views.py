import os.path

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from . import forms
from .models import UploadImage
import cv2
import pytesseract
from django.conf import settings

class ImageToText(View):

    def get(self, request):


        # img = cv2.resize(img, (600, 360))


        my_form = forms.ImageUpload()
        return render(template_name='ocr_api/file_upload.html', context={'form': my_form}, request=request)
        # return HttpResponse(result)

    def post(self, request):
        form = forms.ImageUpload(request.POST, request.FILES)
        im = str(request.FILES['image'])
        print(im, type(im))
        result = 'None'
        if form.is_valid():
            form.save()
            im = im.replace(' ', '_')
            fp = os.path.join(settings.MEDIA_ROOT, 'images/', str(im))
            print(f'full ppath is {fp}')
            img = cv2.imread(fp)
            # print(img)
            # cv2.imshow('im', img)
            # cv2.waitKey(0)


            result = pytesseract.image_to_string(img)

        return render(template_name='ocr_api/show_results.html', context={'text': result}, request=request)


class SearchText(View):

    def post(self, request):
        t_new_r = None
        text = request.POST.get("text")
        query = request.POST.get("query")
        t_new = text.replace(query, f'{query}')
        replace = request.POST.get("replace")
        checked = request.POST.get("replace_chk")
        if checked:
            print('in check')
            t_new_r = t_new.replace(query, replace)
        # print(replace)
        print(checked)
        # print(text)
        # return HttpResponse(t_new)

        return render(
            template_name='ocr_api/search_replaced_result.html',
            context={'text': t_new,
                     'text_replace': t_new_r,
                     },
            request=request
        )


class SearchAndReplaceText(View):

    def get(self, request):
        text = request.GET.get("text")
        replace = request.GET.get("replace")
        print(replace)
        query = request.GET.get("query")
        # print(query)
        # print(text)
        t_new = text.replace(query, f'<b>{query}</b>')
        # print(text)
        return HttpResponse(t_new)

import pathlib
from django.http import FileResponse


class DownloadOutput(View):

    def post(self, request):

        with open('result.txt', 'w+') as f:
            f.write(request.POST.get('text'))
        file_server = pathlib.Path('result.txt')
        if not file_server.exists():
            return HttpResponse('<h1>404: file not found.</h1>')
        else:
            file_to_download = open(str(file_server), 'rb')
            response = FileResponse(file_to_download, content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename="extracted_text.txt"'
            return response
