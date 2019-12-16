import hashlib
import json

import requests
from django.forms import forms, CharField, PasswordInput
from django.shortcuts import render
import time

from .models import *

ip = '192.144.253.99:8080'

def get_all_data():
    cer_set = Certification.objects.all()
    email_set = []
    apply_time_set = []
    deal_time_set = []
    for cer in cer_set:
        id = str(cer.user_id)
        email_set.append(users.objects.filter(_id=id)[0].email)
        apply_time_set.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cer.apply_time / 1000)))
        if cer.deal_time is not 0:
            deal_time_set.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cer.deal_time / 1000)))
        else:
            deal_time_set.append("-")
    email_set.reverse()
    apply_time_set.reverse()
    deal_time_set.reverse()
    return cer_set, email_set, apply_time_set, deal_time_set


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
            return render(request, 'check_cer.html', {'cer_set': data[0], 'email_set': data[1],
                                                      'apply_time_set':data[2], 'deal_time_set':data[3]})
        else:
            return render(request, 'login.html', {'login_error': 'Username or password wrong.'})
    return render(request, 'login.html')


def deal(request, _id):
    obj = Certification.objects.filter(_id=_id)[0]
    return render(request, 'certificate.html', {'cer': obj})


def refuse(request, _id):
    Certification.objects.filter(_id=_id).update(state="not pass")
    Certification.objects.filter(_id=_id).update(deal_time=int(time.time() * 1000))
    data = get_all_data()
    return render(request, 'check_cer.html', {'f_message':'Refuse successfully.',
                                              'cer_set': data[0], 'email_set': data[1],
                                              'apply_time_set':data[2], 'deal_time_set':data[3]})


def certificate(request, _id):
    if request.method == 'POST':
        if_in_database = request.POST.get('if_in_database')
        if if_in_database == 'on':
            try:
                expert_id = request.POST.get('expert_id')
                url = 'http://'+ ip +'/v1/experts/certificateExpert/' + expert_id + '/?' + 'userid=' + _id
                response = requests.get(url=url)
                Certification.objects.filter(_id=_id).update(state="Pass")
                Certification.objects.filter(_id=_id).update(deal_time=int(time.time() * 1000))
                users.objects.filter(_id=_id).update(type=expert_id)
                data = get_all_data()
                return render(request, 'check_cer.html', {'s_message':'certification success.',
                                                          'cer_set': data[0], 'email_set': data[1],
                                                          'apply_time_set':data[2], 'deal_time_set':data[3]})
            except Exception:
                data = get_all_data()
                return render(request, 'check_cer.html', {'f_message': 'Certification failed.',
                                                          'cer_set': data[0], 'email_set': data[1],
                                                          'apply_time_set':data[2], 'deal_time_set':data[3]})
        elif if_in_database == 'off':
            try:
                name = request.POST.get('name')
                n_pubs = request.POST.get('n_pubs')
                pubs = eval(request.POST.get('pubs'))
                orgs = eval(request.POST.get('orgs'))
                org = orgs[-1] if len(orgs) != 0 else ""
                n_citation = request.POST.get('n_citation')
                h_index = request.POST.get('h_index')
                tags = eval(request.POST.get('tags'))
                data = {'name': name, 'n_pubs':int(n_pubs), 'pubs':pubs, 'org':org,
                        'orgs':orgs, 'n_citation':int(n_citation), 'h_index':int(h_index), 'tags':tags,
                        'isCertification':str(_id)}
                url = 'http://' + ip + '/v1/experts/'
                response = requests.post(url=url, data=json.dumps(data))
                Certification.objects.filter(_id=_id).update(state="Pass")
                Certification.objects.filter(_id=_id).update(deal_time=int(time.time() * 1000))
                users.objects.filter(_id=_id).update()
                data = get_all_data()
                return render(request, 'check_cer.html', {'s_message':'certification success.',
                                                          'cer_set': data[0], 'email_set': data[1],
                                                          'apply_time_set':data[2], 'deal_time_set':data[3]})
            except Exception:
                data = get_all_data()
                return render(request, 'check_cer.html', {'f_message': 'Certification failed.',
                                                          'cer_set': data[0], 'email_set': data[1],
                                                          'apply_time_set':data[2], 'deal_time_set':data[3]})
        else:
            data = get_all_data()
            return render(request, 'check_cer.html', {'f_message': 'Unknown error.',
                                                      'cer_set': data[0], 'email_set': data[1],
                                                      'apply_time_set':data[2], 'deal_time_set':data[3]})
