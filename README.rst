===============================
    restaurant_choices
===============================

Content
----------
1. Core Dependencies
2. Getting Started
3. DB migrations and updates to data models
4. Starting the server
5. Testing


1. Core Dependencies
--------------------

The repository of the Fueled | Backend Engineer Test for services Class Written in Python/Django

Python Version 3.8

Django Version 3.0.5

MySQL Version 8.0.21


2. Getting Started
------------------
Note: explicit commands may differ depending on your OS.

    1.	Install Python from https://www.python.org/downloads/
    
    2.	Install MySQL from https://dev.mysql.com/downloads/mysql/
    		NOTE: my require your own config for root access.
    
    3.	Pull down the project from https://github.com/mohan488/restaurant_choices
    
    4.	Setup a virtualenv in your preferred fashion e.g.:
    		$ virtualenv -p python3.8 .
    		$ source bin/activate
    
    5.	pip install -r requirements.txt
    
    6.	OPTIONAL: Setup autoenv (dev tool for directory management) by using following commands in project directory:
    		$ touch .env
    		$ echo "source `which activate.sh`" >> ~/.bashrc
    		$ echo "source bin/activate" >> .env
    		$ echo "export PASSWORD={YOUR_MYSQL_PASSWORD}
    	
    7. Create superuser:
    		$ python manage.py createsuperuser
    	
    8.	Setup DB using the commands:
    		$ python manage.py makemigrations
    		$ python manage.py migrate
    		
    9.	Run server by using:
    		$ python manage.py runserver
    		
    10.	Browse localhost:8000/admin/ to view admin console.
    


3. Database Migration:
----------------------
Navigate to the folder containing manage.py and run the following commands in order.
    1.	python manage.py makemigrations
    2.	python manage.py migrate
    3.	python manage.py runserver


4. Running the Server:
----------------------
Navigate to the folder containing manage.py and run the following command. python manage.py runserver navigate to http://127.0.0.1:8000/ to go to the home page..


5. Testing:
-----------

For initial testing with API, swagger integrated with the Django server. To check, Additional fitters use postman collection shared in the repo.
    
    .. image:: imgs/swagger.*
    :align: center
    :scale: 60 %
==========
swagger UI
==========


    $ http://127.0.0.1:8000/services/v1/restaurant?city__icontains=Aber&latitude=57.149453&longitude= -2.172841&userId=1&postcode__iendswith=1XZ&restaurantName__istartswith=Ang

 Above API lists all Restaurants. Based on Geographic location (eg., country, city, postal code, restaurant name), supports all Django Search options 
 (eg., 'in', 'isnull', 'icontains', 'istartswith','iendswith'). returns all favorite user restaurant including remaining restaurant based search and
 ensures that Restaurant not blacklisted by user.

	
