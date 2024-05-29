mkdir -p ./logs/app
touch ./logs/app/app.log
mkdir -p ./logs/task
touch ./logs/task/task.log

source ./venv/bin/activate
# python bg_task.py &
python manage.py