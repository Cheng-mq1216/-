"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from django.views.static import serve
from django.contrib.auth import views as auth_views

from . import settings
from .Index import views

app_name = 'Index'
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.ArticlesList.as_view()),
    url(r'^post/', views.ArticleFormView.as_view(), name='post-article'),
    url(r'articles/(?P<pk>\d+)/$',
        views.ArticleDetail.as_view(), name='article-detail'),

    url(r'users/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user-info'),

    url(r'article_update/(?P<pk>\d+)/$',
        views.ArticleUpdateView.as_view(), name='article-update'),
    url(r'article_delete/(?P<pk>\d+)/$',
        views.ArticleDelete.as_view(), name='article-delete'),

    url(r'comments/(?P<pk>\d+)/$',
        views.CommentDelete.as_view(), name='comment-delete'),


    # 设置登录视图
    # https://docs.djangoproject.com/en/2.1/topics/auth/default/#module-django.contrib.auth.views
    url(r'^login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    url(r'^register/', views.RegisterFormView.as_view(), name='register'),

    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^mdeditor/', include('mdeditor.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
