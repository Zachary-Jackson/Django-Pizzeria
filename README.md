# Django Pizzeria

Built for a presentation, this pizza based social media site is designed to 
teach the basics of Django.

## Starting

1) Create a virtualenv and install the project requirements, which are listed in
`requirements.txt`. The easiest way to do this is with `pip install -r
requirements.txt` while your virtualenv is activated.

2) In order to initialize the database for the project, go into the `pizzeria`
directory. Then run the following command `python manage.py migrate`. This
will run all of the migrations for the project and initialize the database.
There are some custom migrations in place that will create some "starter"
pizzas and ingredients for you automatically.

## Main Directories / Application information

1) accounts -- This Django App controls all of the User activity. Allowing the
user to login, logout, and signup for an account

2) pizzeria -- All of the backend settings live here

3) static -- All of the "global" project wide static files
(CSS, JavaScript, Images) live here. This is virtually empty for this project.

4) templates -- All project wide templates reside in the `templates` directory.
Often times the main "layout.html" resides here

5) workshop -- The main application for the Django Pizzeria project.
Included in here is all of the pizza views, allowing users to create, update,
delete, and like pizzas. (Among other things)

## Application file information

1) admin.py -- This file allows models to be registered with the Admin
Panel. From the Admin Panel objects can be updated as desired. (Say adding
Onions to a pizza)

2) apps.py -- Application specific information like the name goes here

3) forms.py -- Forms for the application reside here. These can be used in
views or with the Admin

4) models.py -- Objects that need to be saved to the database are
defined and expressed here. The Pizza model, for instance, allows Django to
create and update Database tables for the Pizza object holding attributes like
`name`. In order to update the database with a change to a Model use the
command `python manage.py makemigrations [applicatoin name]`, then run the
migrations with `python manage.py migrate`.

5) test.py -- Unit Testing for an application reside here. All project tests
can be run with the `python manage.py test` command.

6) urls.py -- This file holds all of the URL information like the routes, and
namespaces for each route. Applications's urls are usually imported and used
in the main urls.py file. In this case located in `pizzeria/urls.py`.

7) views.py -- Holds all of the logic for a *view*. Views define what logic
is needed for the user. Processing model objects, handling forms, rendering 
templates, and API calls are handled here.

## Requirements

In addition to the requirements.txt file, python 3.5 + is required due to 
type hinting.