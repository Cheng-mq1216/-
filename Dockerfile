FROM python:3.6

# 创建工作目录
RUN mkdir /code

#设置工作目录
WORKDIR /code

# 安装依赖
COPY . .
COPY ./config/pip.conf /etc/pip.conf

# 切换到生产模式
RUN mv config/production_settings.py app/settings.py

# 安装依赖
RUN pip install -r requirements/production.txt 
