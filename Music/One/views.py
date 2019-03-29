from django.shortcuts import render
from One.music import *
from django.http import JsonResponse,HttpResponseRedirect
from One.models import User
import hashlib

# Create your views here.


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def cookieValid(fun):
    def inner(request, *args, **kwargs):
        cookie = request.COOKIES
        user = User.objects.filter(username=cookie.get("username"))
        session = request.session.get("username")
        if user and session == user.first().username:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/music/login/")
    return inner


@cookieValid
def music(request):
    data = {}
    user = request.COOKIES.get('username')
    data['user'] = user
    return render(request, 'one/index.html', {'data': data})


def login(request):
    data = {"data": ""}
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        user = User.objects.filter(username=username).first()
        if user:
            password = setPassword(request.POST.get("password"))
            db_password = user.password
            if password == db_password:
                response = HttpResponseRedirect("/music/find_music/")
                response.set_cookie("username", user.username)
                request.session["username"] = user.username
                return response
            else:
                data["data"] = "密码错误"
        else:
            data["data"] = "用户不存在"
    return render(request, "one/login.html", {"data": data})


def logout(request):
    response = HttpResponseRedirect("/music/login/")
    response.delete_cookie("username")
    del request.session["username"]
    return response


def music_pc(request):
    if request.method == 'GET' and request.GET:
        name = request.GET.get('s_name')
        s_from = request.GET.get('s_from')
        if s_from == 'kugou':
            all_music = kugou(name)
        elif s_from == 'qianqian':
            all_music = qianqian(name)
        elif s_from == 'migu':
            all_music = migu(name)
    return JsonResponse({"result": all_music})


def register(request):
    if request.method == "POST" and request.POST:
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = User()
        user.username = username
        user.password = setPassword(password)
        user.save()
        return HttpResponseRedirect('/music/login/')
    return render(request, 'one/register.html')


def username_var(request):
    if request.method == 'GET' and request.GET:
        username = request.GET.get('username')
        user = User.objects.filter(username=username)
        if user:
            return JsonResponse({"result": "F"})
        else:
            return JsonResponse({"result": "T"})

