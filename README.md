# ExpenseTrackerApp #

# virtual environment
python3 -m venv myenv 

source myenv/bin/activate; 

# Instaling Django

pip install django   

# ImageField, Django model requires the Pillow library if not installed run

python -m pip install Pillow

# running the migrations

python manage.py makemigrations

python manage.py migrate

# running app

python manage.py runserver
