from django.shortcuts import render, redirect
from .models import *
from .serializers import SaveVocabSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@action(detail=True, methods=['post'])
class SaveVocabViewSet(viewsets.ModelViewSet):
    queryset = SaveVocab.objects.all()
    serializer_class = SaveVocabSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def save_vocab(self, request):
        word_data = request.data.get('word')
        definition_data = request.data.get('definition')
        checked_data = request.data.get('checked')

        save_vocab = SaveVocab.objects.create(word=word_data, definition=definition_data, checked=checked_data)
        save_vocab.save() # Optional?
        return Response({'message': 'Vocab saved'}, status=status.HTTP_201_CREATED)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = UserCreationForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'message': 'Registration successful', 'user': user.username}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'user': user.username, "token": token.key}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)