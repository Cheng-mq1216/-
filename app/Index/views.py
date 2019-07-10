# 加密算法包
import hashlib

# 导入分页插件包
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render

# 引入模型
from .models import Article, Category, Leave, User

# Create your views here.


def index(request):
    # 添加中间导航
    categorys = Category.objects.all()
    articles = Article.objects.all()
    # session 判断 是否登录来区分用户界面
    user = current_log(request)

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
        'user': user
    })


def details(request):
    user = current_log(request)

    if request.method == 'GET':
        # leave = Leave.objects.all()
        id = request.GET.get('id')
        article = Article.objects.get(id=id)
        leave = Leave.objects.filter(article=article)
        return render(request, 'details.html', {
            'article': article,
            'user': user,
            'leave': leave
        })

    if request.method == 'POST':
        if not user:
            return redirect('/login/')
        content = request.POST.get("content")
        article_id = request.POST.get("article")
        article = Article.objects.get(id=article_id)
        Leave.objects.create(content=content, user=user, article=article)
        return redirect('/details/?id=' + article_id)


def post(request):
    # session 判断 是否登录来区分用户界面
    user = current_log(request)
    if not user:
        return redirect('/login/')

    if request.method == 'GET':
        categorys = Category.objects.all()
        return render(request, 'post.html', {
            "categorys": categorys,
            'user': user,
        })

    elif request.method == 'POST':
        title = request.POST.get("title")
        category_name = request.POST.get("category")
        category = Category.objects.get(name=category_name)
        content = request.POST.get("content")
        ret = Article.objects.create(
            title=title, category=category, content=content, user=user)
        return redirect('/index/')


def login(request):

    user = current_log(request)
    if user:
        return redirect('/index/')

    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        sha256 = hashlib.sha256(bytes('加一些东西', encoding='utf8') + b'lxgzhw')
        sha256.update(bytes(password, encoding='utf8'))
        password = sha256.hexdigest()
        ret = User.objects.filter(name=username, password=password)

        if not ret:
            return render(request, 'login.html', {'error': '错误，无法登陆'})

        # 登录成功
        request.session['username'] = username
        return redirect('/index/')


def logout(request):
    del request.session['username']
    return redirect('/index/')


def user(request):
    user = current_log(request)
    articles = Article.objects.filter(user=user)
    return render(request, 'user.html', {'user': user,'articles':articles})


# 注册视图函数
def register(request):
    if current_log(request):
        return redirect('/index/')

    if request.method == 'GET':
        return render(request, 'register.html')

    elif request.method == 'POST':
        # 获取前端数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        try:
            assert password == password1
            if User.objects.filter(name=username):
                raise Exception()
        except AssertionError:
            error = '校验错误'
        except Exception as e:
            error = "用户名重复！"
        else:  # 成功
            sha256 = hashlib.sha256(
                bytes('加一些东西', encoding='utf8') + b'lxgzhw')
            sha256.update(bytes(password, encoding='utf8'))
            password = sha256.hexdigest()
            User.objects.create(name=username, password=password)
            return redirect('/login/')

        return render(request, 'register.html', {
            "error": error
        })

        if username and password and password == password1:
            if User.objects.filter(name=username):
                return render(request, 'register.html', {
                    error: "用户名重复！"
                })


def current_log(request):
    username = request.session.get('username')
    if username:
        return User.objects.get(name=username)
