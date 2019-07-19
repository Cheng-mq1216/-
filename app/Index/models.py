from django.db import models
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User

# Create your models here.

# 分类表


class Category(models.Model):
    name = models.CharField(max_length=24, verbose_name="名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "分类表"


# 文章表
class Article(models.Model):
    img = models.ImageField(
        verbose_name='头图', upload_to='articles', blank=True)
    title = models.CharField(max_length=24, verbose_name='标题')
    category = models.ForeignKey(
        Category, verbose_name="分类", on_delete=models.CASCADE)
    description = models.CharField(
        max_length=128, verbose_name="文章描述", blank=True)
    author = models.ForeignKey(
        User, verbose_name="作者", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    content = MDTextField(verbose_name="内容")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = verbose_name = "文章表"


# 评论表
class Comment(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    content = models.TextField(max_length=500, verbose_name="内容")
    article = models.ForeignKey(
        Article, verbose_name="文章", on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, verbose_name="评论作者", on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]

    class Meta:
        verbose_name_plural = verbose_name = "留言表"
