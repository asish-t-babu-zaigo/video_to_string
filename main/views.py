from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import moviepy.editor
from today.settings import mydomain
import speech_recognition as sr




@api_view(['POST'])
def video_to_text(request):
    print(request.data)
    if request.method =="POST":
        serializer=VideoSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()   
            file=serializer.data['file']
            print(file)
            file=f"{mydomain}{file}".replace("//static","/static")
            print(file)
            video = moviepy.editor.VideoFileClip(file)
            audio = video.audio
            
            a=Video.objects.count()+1
            b="audio"+str(a)+".wav"
            audio.write_audiofile("./static/audio"+str(a)+".wav")
            try:
                recognizer = sr.Recognizer()
                audio = sr.AudioFile("./static/"+b)
                with audio as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                print(text)
                return Response({'text':text})
            except:
                return Response({"error" : "unsupported language"})
        return Response(serializer.errors)

@api_view(['GET'])
def my_view(request,id):
    video=Video.objects.get(id=id)
    serializer=VideoSerializer(video)
    file=serializer.data['file']
    file=f"{mydomain}{file}".replace("//static","/static")
    return Response({"file":file})

# def my_view(request):
#     return render(request,'html.html')
