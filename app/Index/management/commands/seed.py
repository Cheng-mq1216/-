"""
生成中文的数据库随机数据。

警告 ：仅用于开发环境
WARNING !! ONLY USE THIS IN DEVELOPMENT MODE
"""
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import UserManager
from faker import Faker

from ...models import Article, Category, Leave, User


class Command(BaseCommand):
    help = 'Seeds the database.'

    manager = get_user_model()._default_manager.db_manager('default')
    if manager.filter(username='root'):
        manager.get(username='root').delete()
    
    manager.create_superuser(
            username='root', email='root@mail.com', password='root')

    print('Admin root用户已生成，密码为root')
    print('WARNING: 请勿在生产环境下使用本脚本')

    def handle(self, *args, **options):

        fake = Faker('zh-cn')
        categorys = [Category.objects.create(
            name=fake.word()) for _ in range(10)]

        users = [User.objects.create(
            name=fake.name(), password=fake.password()
        ) for _ in range(10)]

        articles = [Article.objects.create(
            title=fake.company_prefix(),
            category=random.choice(categorys),
            content=fake.text(max_nb_chars=600),
            user=random.choice(users)
        ) for _ in range(20)]

        leaves = [Leave.objects.create(
            article=random.choice(articles),
            content=fake.text(),
            user=random.choice(users)
        ) for _ in range(100)]
