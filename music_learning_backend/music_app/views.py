from django.shortcuts import render
from rest_framework import viewsets
from .models import Song, UserProgress
from .serializer import SongSerializer, UserProgressSerializer

# Create your views here.
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer