# 加密算法包
import hashlib

# 导入分页插件包
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render

# 引入模型
from .models import Articles, Category, Leave, Users

# Create your views here.


def index(request):
    # 添加中间导航
    categorys = Category.objects.all()
    articles = Articles.objects.all()
    # session 判断 是否登录来区分用户界面
    user = current_log(request)
    if user:
        status = True
    else:
        status = False
    # # 分页的实现
    # p = request.GET.get('p')  # 在URL中获取当前页面数
    # paginator = Paginator(articles, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    # try:
    #     articles = paginator.page(p)  # 获取当前页码的记录
    # except PageNotAnInteger:
    #     articles = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    # except EmptyPage:
    #     articles = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'index.html', {
        'articles': articles,
        'categorys': categorys,
        'status': status,
    })


def details(request):
    # session 判断 是否登录来区分用户界面
    leave = Leave.objects.all()
    number = len(leave)
    user = current_log(request)
    if user:
        status = True
    else:
        status = False
    id = request.GET.get('id')
    print(id)
    article = Articles.objects.get(id=id)
    return render(request, 'details.html', {
        'article': article,
        'status': status,
        'leave': leave,
        # 'articles':leave,
        'number': number,
    })


def leave(request):
    leave = Leave.objects.all()
    number = len(leave)
    # 分页的实现
    # p = request.GET.get('p')
    # paginator = Paginator(leave, 5)
    # try:
    #     leave = paginator.page(p)
    # except PageNotAnInteger:
    #     leave = paginator.page(1)
    # except EmptyPage:
    #     leave = paginator.page(paginator.num_pages)
    return render(request, 'details.html', {
        'leave': leave,
        # 'articles':leave,
        'number': number
    })


def post(request):
    # session 判断 是否登录来区分用户界面
    user = current_log(request)
    if user:
        status = True
    else:
        status = False

    categorys = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get("title")
        category = request.POST.get("category")
        category = Category.objects.create(name=category)
        content = request.POST.get("content")
        ret = Articles.objects.create(title=title,
                                      category=category, content=content)
        if ret:
            return redirect('/index/')
    return render(request, 'post.html', {
        "categorys": categorys,
        'status': status,
    })


def login(request):
    # 写判断
    # 去数据库查,有没有对应的用户
    status = '未操作，无状态'
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        sha256 = hashlib.sha256(bytes('加一些东西', encoding='utf8') + b'lxgzhw')
        sha256.update(bytes(password, encoding='utf8'))
        password = sha256.hexdigest()
        # 查询
        ret = Users.objects.filter(username=username, password=password)
        print(ret)
        if ret:
            request.session['login'] = True
            request.session['username'] = username
            username = request.session.get('username')
            # #通过get方法可以获得单个对象中的属性
            # test = Users.objects.get(username = username)
            # print('----------------')
            # print(test.id)
            # request.session['password'] = password
            return redirect('/index/')
        else:
            status = '错误，无法登陆'

    return render(request, 'login.html', {'status': status})


def logout(request):
    del request.session['username']
    return redirect('/index/')


def user(request):
    user = current_log(request)
    if user:
        status = True
    else:
        status = False
    username = user.username
    return render(request, 'user.html', {'username': username, 'status': status})


# 注册视图函数
def register(request):
    # print('aaaaaaaaa')
    # 把前端的数据接收过来,保存到数据库
    if request.method == 'POST':
        # 获取前端数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        # 打印测试
        # print(username, password, password1)
        # 存到数据库
        if username and password and password == password1:
            # 判断
            # print('OK')
            sha256 = hashlib.sha256(
                bytes('加一些东西', encoding='utf8') + b'lxgzhw')
            sha256.update(bytes(password, encoding='utf8'))
            password = sha256.hexdigest()
            print(password)
            # 保存到数据库
            ret = Users.objects.create(username=username, password=password)
            # print('OK')
            if ret:
                # 成功了
                return redirect('/login/')

    return render(request, 'register.html')

# session 函数，判断用户


def current_log(request):
    username = request.session.get('username')
    if username:
        return Users.objects.get(username=username)
