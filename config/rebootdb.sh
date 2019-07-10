rm -rf data/**
docker-compose restart db
docker-compose exec web config/wait-for-it.sh db:3306 -- python manage.py migrate
