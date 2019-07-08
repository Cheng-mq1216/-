if [ ! -f .env ]; then
    echo "[Error!] 没有检测到.env配置文件，退出。"
    exit -1
fi
source .env

# echo '* * * 开始推送镜像 * * *'
# echo '推送至阿里云容器镜像仓库：北京'
# docker login --username=$USERNAME --password-stdin registry.cn-beijing.aliyuncs.com <<< $PASSWD
# docker push "registry.cn-beijing.aliyuncs.com/${USERNAME}/production-practice"
# echo '* * * 推送镜像成功 * * *'

echo '* * * 开始远程部署 * * *'
scp .env $SERVER_NAME:~
ssh $SERVER_NAME -tt << __EOF__ 

if not command -v git >/dev/null 2>&1; then 
  echo '远程机器上不存在Git，退出' 
  exit
fi

if not command -v docker-compose >/dev/null 2>&1; then 
  echo '远程机器上不存在docker-compose，退出' 
  exit
fi

if [ ! -d production-practice ]; then
    git clone https://github.com/Cheng-mq1216/production-practice
fi

cd production-practice
git checkout origin/deploy
git pull
mv ../.env .
docker-compose up -d
__EOF__  

echo '* * * 部署完毕 * * *'