from rest_framework import serializers
from .models import *

class SaveVocabSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveVocab
        fields = '__all__'