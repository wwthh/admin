import hashlib
import json

import requests
from django.forms import forms, CharField, PasswordInput
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .models import *


def encrypt_md5(s):
    m = hashlib.md5()
    m.update(s.encode(encoding='utf-8'))
    return m.hexdigest()


class UserForm(forms.Form):
    username = CharField(label='username', max_length=100)
    password = CharField(label='password', widget=PasswordInput())


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = encrypt_md5(request.POST.get('password'))
        if username == 'Manager' and password == "a68ae8cb01ff58d13b6cb431d6628543":
            cer_set = Certification.objects.all()
            email_set = []
            for cer in cer_set:
                id = cer.user_id.split('\"')[1]
                email_set.append(users.objects.filter(_id=id)[0].email)
            email_set.reverse()
            return render(request, 'check_cer.html', {'cer_set': cer_set, 'email_set': email_set})
        else:
            return render(request, 'login.html', {'login_error': 'Username or password wrong.'})
    return render(request, 'login.html')


def deal(request, _id):
    obj = Certification.objects.filter(_id=_id)[0]
    return render(request, 'certificate.html', {'cer': obj})


def certificate(request):
    if request.method == 'POST':
        if_in_database = request.POST.get('if_in_database')
        if if_in_database == 'on':
            try:
                expert_id = request.POST.get('expert_id')
                url = 'http://ip:port/v1/experts/certificateExpert/' + expert_id
                requests.get(url)
                return render(request, 'certificate.html', {'s_message':'certification success.'})
            except Exception:
                return render(request, 'certificate.html', {'f_message': 'Certification failed.'})
        elif if_in_database == 'off':
            try:
                name = request.POST.get('name')
                n_pubs = request.POST.get('n_pubs')
                pubs = request.POST.get('pubs')
                n_orgs = request.POST.get('n_orgs')
                orgs = request.POST.get('orgs')
                n_citation = request.POST.get('n_citation')
                h_index = request.POST.get('h_index')
                tags = request.POST.get('tags')
                data = {'name': name, 'n_pubs':n_pubs, 'pubs':pubs, 'n_orgs':n_orgs,
                        'orgs':orgs, 'n_citation':n_citation, 'h_index':h_index, 'tags':tags}
                url = 'http://ip:port/v1/experts/'
                requests.post(url, data=data)
                return render(request, 'certificate.html', {'s_message':'certification success.'})
            except Exception:
                return render(request, 'certificate.html', {'f_message': 'Certification failed.'})
        else:
            return render(request, 'certificate.html', {'f_message': 'Unknown error.'})
