# expensify-app

To start the server, access the command line in the project driectory. Enter "python manage.py runserver"

To access the home page, navigate to http://127.0.0.1:8000/reports

To access the admin page, you will need to create an admin account. From the command line, enter "python manage.py createsuperuser" and enter the requested information. Then you can go to http://127.0.0.1:8000/admin/.

Right now, you can create budget categories (food, entertainment, etc.), add/edit income (amount, date, name), add/edit expenses (amount, date, category, name), and view a category breakdown in the form of a pie chart. 

Features to come:
  - Edit categories
  - Add new categories from "add/edit expense" screen
