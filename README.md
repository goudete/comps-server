# comps-server

Steps to run locally

- Make sure python and pip are installed locally
- Create a virtual environment 
- Activate virtual environment
- cd into server
- run $ pip install -r requirements.txt (this downloads all dependencies into virtual env)
- run $ python manage.py makemigrations
- run $ python manage.py migrate
- run $ python manage.py runserver
- Create 10 users through signup page
- run $ python manage.py loaddata places.json
- run $ python manage.py loaddata ratings.json

The data should be loaded up and the the server should be running on port localhost:8000
Make sure to follow the ReadMe in the comps-client repo as well

