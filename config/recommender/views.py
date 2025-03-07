from django.shortcuts import render
from .models import *
from .serializers import SaveVocabSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.
@action(detail=True, methods=['post'])
class SaveVocabViewSet(viewsets.ModelViewSet):
    queryset = SaveVocab.objects.all()
    serializer_class = SaveVocabSerializer
    
    def save_vocab(self, request):
        word_data = request.data.get('word')
        definition_data = request.data.get('definition')
        checked_data = request.data.get('checked')

        save_vocab = SaveVocab.objects.create(word=word_data, definition=definition_data, checked=checked_data)
        save_vocab.save() # Optional?
        return Response({'message': 'Vocab saved'}, status=status.HTTP_201_CREATED)