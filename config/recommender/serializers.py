from rest_framework import serializers
from .models import *

class SaveVocabSerializer(serializers.ModelSerializer):
    reviewed = serializers.BooleanField(source='checked', required=False)

    class Meta:
        model = SaveVocab
        fields = ('id', 'word', 'definition', 'save_date', 'reviewed')