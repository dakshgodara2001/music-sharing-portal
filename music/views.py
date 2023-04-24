from itertools import chain

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse

from users.models import Friend
from .forms import AlbumForm, SongForm
from .models import Album, Song, Shared_album
from django.contrib.auth.models import User

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_album(request):
    if not request.user.is_authenticated:
        return render(request, '../templates/users/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.is_private = form.cleaned_data['is_private']
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, '../templates/music/create_album.html', context)
            album.save()
            return render(request, '../templates/music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, '../templates/music/create_album.html', context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, '../templates/music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, '../templates/music/create_song.html', context)
        album.total_songs = album.total_songs + 1
        album.save()
        song.save()
        return render(request, '../templates/music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, '../templates/music/create_song.html', context)


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    followee = Friend.objects.filter(follower=request.user)
    friends_albums = []
    for follo in followee:
        x = Album.objects.filter(Q(user=follo.followee)).exclude(is_private=True)
        friends_albums = chain(friends_albums, x)

    received_albums = Shared_album.objects.filter(receiver=request.user)
    public_albums = Album.objects.exclude(user=request.user).filter(is_private=False)
    context = {
        'albums': albums,  # unique albums
        'received_albums': received_albums,
        'public_albums': public_albums,
        'friends_albums': friends_albums
    }
    return render(request, 'users/index.html', context)


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    album.total_songs -= 1
    album.save()
    song.delete()
    return render(request, '../templates/music/detail.html', {'album': album})


def detail(request, album_id):
    if not request.user.is_authenticated:
        return render(request, '../templates/users/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, '../templates/music/detail.html', {'album': album, 'user': user})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, '../templates/users/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, '../templates/music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })

def toggle(request,album_id):
    print("inside toggle")
    w = get_object_or_404(Album, pk=album_id)
    w.is_private = not w.is_private
    w.save()
    user = request.user
    album = get_object_or_404(Album, pk=album_id)
    return render(request, '../templates/music/detail.html', {'album': album, 'user': user})


def share_album(request, album_id):
    album = get_object_or_404(Album,pk=album_id)
    already_shared_users = Shared_album.objects.filter(album_title=album)
    all_users_objects = User.objects.exclude(username=request.user.username)
    
    all_users = []
    for u in all_users_objects:
        all_users.append(u.username)

    shared_users_list = []
    for u in already_shared_users:
        shared_users_list.append(u.receiver.username)

    unshared_users = list(set(all_users) - set(shared_users_list))

    context = {
        "shared_users": shared_users_list,
        "unshared_users":unshared_users,
        "album_id": album_id
    }
    return render(request,'../templates/music/share_album.html',context)

def share_album_detail(request, album_id):
    if not request.user.is_authenticated:
        return render(request, '../templates/users/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, '../templates/music/shared_album_detail.html', {'album': album, 'user': user})


def share(request,album_id,username):
    album = get_object_or_404(Album,pk=album_id)
    receiver = get_object_or_404(User,username=username)
    Shared_album.objects.create(owner=request.user,receiver=receiver,album_title=album)
    return share_album(request,album_id)

def unshare(request,album_id,username):
    album = Shared_album.objects.filter(receiver__username=username,album_title=get_object_or_404(Album,pk=album_id))
    print(album)
    album.delete()
    return share_album(request,album_id)