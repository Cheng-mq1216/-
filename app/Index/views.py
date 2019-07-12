# 加密算法包
import hashlib

from django import forms

# 导入权限控制类
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# 导入分页插件包
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.urls import reverse

# 导入请求上下文模版
from django.template import RequestContext

# 导入快捷函数
from django.shortcuts import Http404, redirect, render, render_to_response

# 导入模型视图
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView, FormMixin

# 导入Markdown渲染插件
from markdown import markdown

# 导入模型
from .models import Article, Category, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class UserDetail(DetailView):
    model = User
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = self.object.article_set.all()
        context['form'] = CommentForm()
        return context


class RegisterFormView(FormView):
    """注册页面。使用系统提供的创建用户表单。"""
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        """校验成功，保存用户。"""
        form.save()
        return super().form_valid(form)


class ArticlesList(ListView):
    """处理多篇文章的显示。"""
    model = Article
    queryset = Article.objects.order_by('-time')
    context_object_name = 'articles'
    template_name = 'index.html'
    paginate_by = 5


class ArticleDetail(DetailView, FormMixin):
    """处理单篇文章详情页的显示。
    以及所有留言的显示
    FormMixin 处理留言的上传 。
    """
    model = Article
    context_object_name = 'article'
    template_name = 'details.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('article-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all()
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        a = form.save(commit=False)
        a.author = self.request.user
        a.article = self.object
        a.save()
        return super().form_valid(form)


class ArticleFormView(FormView):
    """处理添加 Article 时的表单"""

    model = Article
    template_name = 'post.html'
    context_object_name = 'articles'
    form_class = ArticleForm
    success_url = '/'

    def form_valid(self, form):
        a = form.save(commit=False)
        a.author = self.request.user
        a.save()
        return super().form_valid(form)


class ArticleUpdateView(UpdateView, LoginRequiredMixin):
    """处理更新Article时的表单"""
    model = Article
    success_url = '/'
    fields = ['content']
    template_name = 'update.html'


class ArticleDelete(DeleteView, LoginRequiredMixin):
    """处理删除Article的操作"""
    model = Article
    success_url = '/'


class CommentView(CreateView):
    """处理评论的表单"""
    model = Comment
    fields = ['content', 'author']


class CommentDelete(DeleteView, LoginRequiredMixin):
    """删除评论的操作"""
    model = Comment

    def get_success_url(self):
        return reverse('article-detail', kwargs={'pk': self.object.article.pk})
