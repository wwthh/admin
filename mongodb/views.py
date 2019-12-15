import hashlib
import json

import requests
from bson import ObjectId
from django.forms import forms, CharField, PasswordInput
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import datetime

from .models import *

def get_all_data():
    cer_set = Certification.objects.all()
    email_set = []
    for cer in cer_set:
        id = cer.user_id.split('\"')[1]
        email_set.append(users.objects.filter(_id=id)[0].email)
    email_set.reverse()
    return cer_set, email_set


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
            data = get_all_data()
            return render(request, 'check_cer.html', {'cer_set': data[0], 'email_set': data[1]})
        else:
            return render(request, 'login.html', {'login_error': 'Username or password wrong.'})
    return render(request, 'login.html')


def deal(request, _id):
    obj = Certification.objects.filter(_id=_id)[0]
    return render(request, 'certificate.html', {'cer': obj})


def refuse(request, _id):
    Certification.objects.filter(_id=_id).update(state="not pass")
    Certification.objects.filter(_id=_id).update(deal_time=datetime.datetime.now())
    data = get_all_data()
    return render(request, 'check_cer.html', {'f_message':'Refuse successfully.',
                                              'cer_set': data[0], 'email_set': data[1]})


def certificate(request, _id):
    if request.method == 'POST':
        if_in_database = request.POST.get('if_in_database')
        if if_in_database == 'on':
            try:
                expert_id = request.POST.get('expert_id')
                # url = 'http://ip:port/v1/experts/certificateExpert/' + expert_id
                # requests.get(url)
                Certification.objects.filter(_id=_id).update(state="Pass")
                Certification.objects.filter(_id=_id).update(deal_time=datetime.datetime.now())
                data = get_all_data()
                return render(request, 'check_cer.html', {'s_message':'certification success.',
                                                          'cer_set': data[0], 'email_set': data[1]})
            except Exception:
                data = get_all_data()
                return render(request, 'check_cer.html', {'f_message': 'Certification failed.',
                                                          'cer_set': data[0], 'email_set': data[1]})
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
                data = get_all_data()
                return render(request, 'check_cer.html', {'s_message':'certification success.',
                                                          'cer_set': data[0], 'email_set': data[1]})
            except Exception:
                data = get_all_data()
                return render(request, 'check_cer.html', {'f_message': 'Certification failed.',
                                                          'cer_set': data[0], 'email_set': data[1]})
        else:
            data = get_all_data()
            return render(request, 'check_cer.html', {'f_message': 'Unknown error.',
                                                      'cer_set': data[0], 'email_set': data[1]})
