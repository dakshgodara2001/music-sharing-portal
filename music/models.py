from django.contrib.auth.models import Permission, User
from django.db import models


class Album(models.Model):
    user = models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField(upload_to="album_logos/")
    is_favorite = models.BooleanField(default=False)
    is_private = models.BooleanField(default=True,help_text="Is this a private album ? ")
    total_songs = models.IntegerField(default=0)
    shared = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(upload_to="songs/")
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

class Shared_album(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_album_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='%(class)s_album_receiver')
    album_title = models.ForeignKey(Album,on_delete=models.CASCADE)
