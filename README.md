# Minisite version 1.1
1. The first thing to do is to clone the repository:
2. Create a virtual environment to install dependencies in and activate it:
3. Then install the dependencies:
    (env) pip install -r requirements.txt
4. Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

Once pip has finished downloading the dependencies:
5. Run:
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py runserver
6. And navigate to http://127.0.0.1:8000/.