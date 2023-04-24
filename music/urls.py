from . import views
from django.urls import path, include

from .views import toggle

app_name = 'music'

urlpatterns = [
    
    path('toggle/(<album_id>)', views.toggle, name='toggle'),
    path('(<album_id>[0-9]+)/', views.detail, name='detail'),
    path('(<song_id>[0-9]+)/favorite/', views.favorite, name='favorite'),
    path('songs/(<filter_by>[a-zA_Z]+)/', views.songs, name='songs'),
    path('create_album/', views.create_album, name='create_album'),
    path('(<album_id>[0-9]+)/create_song/', views.create_song, name='create_song'),
    path('(<album_id>[0-9]+)/delete_song/(<song_id>[0-9]+)/', views.delete_song, name='delete_song'),
    path('(<album_id>[0-9]+)/favorite_album/', views.favorite_album, name='favorite_album'),
    path('(<album_id>[0-9]+)/delete_album/', views.delete_album, name='delete_album'),
    path('(<album_id>[0-9]+)/share_album/', views.share_album, name='share_album'),
    path('(<album_id>[0-9]+)', views.share_album_detail, name='share_album_detail'),
    path('share/(<album_id>[0-9]+)/(<username>[\w\-]+)/', views.share, name="share"),
    path('unshare/(<album_id>[0-9]+)/(<username>[\w\-]+)/', views.unshare, name="unshare"),
]

