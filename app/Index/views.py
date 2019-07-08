from django.shortcuts import render, redirect
# 导入分页插件包
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 引入模型
from .models import Articles, Users, Category
# 加密算法包
import hashlib
# Create your views here.
def index(request):
    # 添加中间导航
    categorys = Category.objects.all()
    articles = Articles.objects.all()
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
    })


def details(request):
    id = request.GET.get('id')
    print(id)
    article = Articles.objects.get(id=id)
    return render(request, 'details.html', {
        'article': article
    })


def leave(request):
    return render(request, 'leave.html')

def post(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        ret = Users.objects.filter(title=title,content=content)
        if ret:
             return redirect('/index/')
    return render(request, 'post.html')

def login(request):
    # 写判断
    # 去数据库查,有没有对应的用户
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
            return redirect('/index/')

    return render(request, 'login.html')

def user(request):
      return render(request, 'user.html')


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
            sha256 = hashlib.sha256(bytes('加一些东西', encoding='utf8') + b'lxgzhw')
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
