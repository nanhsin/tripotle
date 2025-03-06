from django.db import models

# Create your models here.
class SaveVocab(models.Model):
    word = models.CharField(max_length=100)
    definition = models.TextField()
    save_date = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.word