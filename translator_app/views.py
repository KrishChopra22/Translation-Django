from django.shortcuts import render, redirect
import sys
import os
from django.http import FileResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings as django_settings
from django.core.files.storage import default_storage
from urllib import parse
from .models import AudioModel
import speech_recognition as sr
from googletrans import Translator
import gtts
import base64

r = sr.Recognizer()


def TTSHome(request):
    # python3

    if request.is_ajax():
        print('a===>>>>>', request.GET.get('datas'))
        print('a===>>>>>', request.FILES.get('datas'))
        print('a===>>>>>', request.GET.get('datas'))


    if request.method == 'POST':
        file = request.FILES.get('file')
        lang = request.POST.get('lang')
        dlang = request.POST.get('dlang')
        aobj = AudioModel()
        aobj.audioname = 'temp1'
        aobj.audio = file
        aobj.save()
        # Using google to recognize audio
        audio = AudioModel.objects.last()
        adurl = str(audio.audio.url)
        with spr.WavFile(adurl[1:]) as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            text = r.recognize_google(audio, language=dlang)

        translator = Translator()
        ttext = translator.translate(text, src=dlang, dest=lang)

        coded_string = request.POST.get('blobdata')

        sample_string_bytes = coded_string.encode("UTF-8")
        imgdata = base64.b64decode(sample_string_bytes)
        filename = 'some_image.wav'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

        context = {
            'text': ttext,
            'lang': lang,
        }
        return render(request, 'ttshome.html', context)

    context = {

    }
    return render(request, 'ttshome.html', context)

