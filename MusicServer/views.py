from django.shortcuts import render_to_response, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from MusicServer.froms import SignInForm, SignUpForm, TrackForm
from django.template import RequestContext
from MusicServer.models import Track
from django.http import HttpResponse

import os
PROJECT_PATH = os.path.dirname(__file__)
MEDIA_PATH = os.path.join(PROJECT_PATH, 'media')


def index_view(request):
    user = request.user
    if user.is_authenticated():
        uid = user.pk
        return HttpResponseRedirect(reverse('user', kwargs={'uid': uid}))
    context = RequestContext(request)

    sign_in_form = SignInForm()
    sign_up_form = SignUpForm()

    if request.method == 'POST':
        data = request.POST
        if 'sign_up' in data.keys():
            sign_up_form = SignUpForm(data=data)
            if sign_up_form.is_valid():
                username = sign_up_form.clean_username()
                password = sign_up_form.clean_password2()

                User.objects.create_user(username=username, password=password)
                user = authenticate(username=username, password=password)
                login(request, user)
                uid = user.pk
                return HttpResponseRedirect(reverse('user', kwargs={'uid': uid}))
        elif 'sign_in' in data.keys():
            sign_in_form = SignInForm(data=data)
            if sign_in_form.is_valid():
                user = authenticate(username=data['username'], password=data['password'])
                if user is not None:
                    login(request, user)
                    uid = user.pk

                    return HttpResponseRedirect(reverse('user', kwargs={'uid': uid}))

    return render_to_response(
        'MusicServer/login_page.html',
        dict(sign_up_form=sign_up_form, sign_in_form=sign_in_form), context)


def sign_out_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_view(request, uid):
    user = request.user
    context = RequestContext(request)
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    uid = user.pk
    track_form = TrackForm()

    tracks = Track.objects.all()
    # form = Track()
    # return render_to_response('MusicServer/user_page.html', {'form': form})

    my_username = request.user

    return render_to_response('MusicServer/user_page.html', dict(username=my_username, uid=uid, track_form=track_form,
                                                                 tracks=tracks), context)


def handle_uploaded_files(files):
    # track = files['track']
    source = files['source']

    # destination_track = open((os.path.join(MEDIA_PATH, 'tracks\\') + str(track.name)), 'wb+')
    # for chunk in track.chunks():
    #     destination_track.write(chunk)
    # destination_track.close()

    # if source:
    source_path = os.path.join(MEDIA_PATH, 'source\\') + str(source.name)
    destination_source = open(source_path, 'wb+')
    for chunk in source.chunks():
        destination_source.write(chunk)
    destination_source.close()

    # if source:
    #     new_track = Track(name=track.name,
    #                       track_path='/tracks/'+track.name,
    #                       source_path='/source/'+source.name)
    # else:
    new_track = Track.objects.create(name=source.name,
                      source_path=source_path)

    new_track.save()


def upload_track(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    uid = user.pk
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            form = TrackForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_files(request.FILES)
            return HttpResponseRedirect(reverse('user', kwargs={'uid': uid}))

    return HttpResponseRedirect(reverse('user', kwargs={'uid': uid}))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def download_view(request, track_id):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    uid = user.pk
    track = Track.objects.filter(pk=track_id)
    track_path = Track.objects.filter(pk=track_id).values('source_path')[0]['source_path']
    file = open(track_path, 'r')
    response = HttpResponse()
    response.content = file.read()
    response["Content-Disposition"] = "attachment; filename={0}".format(
            track)
    return response

    # return HttpResponseRedirect(reverse('user', kwargs={'uid': uid}))