from django import forms
from django.contrib.auth.models import User
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from .models import Album, Song


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo','is_private']

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['is_private'].label = "Is this a private album ?"

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']