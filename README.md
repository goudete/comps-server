# comps-server

Steps to run locally

1. Clone this repository
2. Make sure python and pip are installed locally
3. Create a virtual environment 
4. Activate virtual environment
5. cd into server
6. run $ pip install -r requirements.txt (this downloads all dependencies into virtual env)
7. run $ python manage.py makemigrations
8. run $ python manage.py migrate
9. run $ python manage.py runserver
10. Create 10 users through signup page
11. run $ python manage.py loaddata places.json
12. run $ python manage.py loaddata ratings.json

The data should be loaded up and the the server should be running on port localhost:8000
Make sure to follow the ReadMe in the comps-client repo as well

