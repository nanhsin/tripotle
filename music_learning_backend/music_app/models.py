from django.db import models

# Create your models here.
class Song(models.Model):
    year = models.IntegerField()
    rank = models.IntegerField()
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    lyrics = models.TextField()
    difficulty_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.year} No.{self.rank} - {self.title} by {self.artist}"

class UserProgress(models.Model):
    user_id = models.IntegerField()
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    words_learned = models.IntegerField(default=0)
    progress_percentage = models.FloatField(default=0.0)
