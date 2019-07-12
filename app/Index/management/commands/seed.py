"""
生成中文的数据库随机数据。

警告 ：仅用于开发环境
WARNING !! ONLY USE THIS IN DEVELOPMENT MODE
"""
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from faker import Faker

from ...models import Article, Category, Comment


class Command(BaseCommand):
    help = 'Seeds the database.'

    def handle(self, *args, **options):
        if User.objects.filter(username='root'):
            User.objects.get(username='root').delete()

        User.objects.create_superuser(
            username='root', email='root@mail.com', password='root')

        print('Admin root用户已生成，密码为root')
        print('WARNING: 请勿在生产环境下使用本脚本')

        category_number = 10
        user_number = 10
        article_number = 20
        comment_number = 100

        fake = Faker('zh-cn')
        categorys = [Category.objects.create(
            name=fake.word()) for _ in range(category_number)]

        users = [User.objects.create(
            username=fake.name(), password=fake.password()
        ) for _ in range(user_number)]

        articles = [Article.objects.create(
            title=fake.company_prefix(),
            category=random.choice(categorys),
            content=fake.text(max_nb_chars=600),
            author=random.choice(users)
        ) for _ in range(article_number)]

        comments = [Comment.objects.create(
            article=random.choice(articles),
            content=fake.text(),
            author=random.choice(users)
        ) for _ in range(comment_number)]

        print("""生成数据：
        category : {}
        user: {}
        articles: {}
        comments: {}
        """.format(category_number, user_number, article_number, comment_number))
