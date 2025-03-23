from django.shortcuts import render, redirect
from .models import *
from .serializers import SaveVocabSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@action(detail=True, methods=['post'])
class SaveVocabViewSet(viewsets.ModelViewSet):
    queryset = SaveVocab.objects.all()
    serializer_class = SaveVocabSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def save_vocab(self, request):
        word_data = request.data.get('word')
        definition_data = request.data.get('definition')
        checked_data = request.data.get('checked')

        save_vocab = SaveVocab.objects.create(word=word_data, definition=definition_data, checked=checked_data)
        save_vocab.save() # Optional?
        return Response({'message': 'Vocab saved'}, status=status.HTTP_201_CREATED)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'recommender/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'recommender/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')