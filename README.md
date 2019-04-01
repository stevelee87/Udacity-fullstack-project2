# Udacity-fullstack-project2
Build a catalog web application implementing CRUD and login session with OAuth2.0

## 1 Introduction

### Project Overview
You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

### Why This Project?
Modern web applications perform a variety of functions and provide amazing features and utilities to their users; but deep down, it’s really all just creating, reading, updating and deleting data. In this project, you’ll combine your knowledge of building dynamic websites with persistent data storage to create a web application that provides a compelling service to your users.

### What Will I Learn?
You will learn how to develop a RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication. You will then learn when to properly use the various HTTP methods available to you and how these methods relate to CRUD (create, read, update and delete) operations.

## 2 Architecture

The main file `application.py` contains the core Flask code, i.e. the app.route decorators. All the CRUD operations are at DAO.py. DAO (_Data Access Object_) file contains 3 classes: DAOUser, DAOCategory and DAOItem, whose methods are called in the `application.py` to get the related CRUD operations done.
The `database_setup.py` file contains the necessary classes to setup a SQLAlchemy database, database tables and their relationships.
The `db_init.py` is just a file to create some first items to populate the database.

## 3 How to run

**Important:** I am using `Python 3.6.8`. Before proceeding, make sure you have a compatible version.

1. Install the necessary Python modules below (I recommend you to create a virtual environment and install all the modules there. I am using _Pipenv_):
 * `Flask 1.0.2`
 * `Flask-SQLAlchemy 2.3.1`
 * `SQLAlchemy 1.3.1`
 * `oauth2client 4.1.3`
 * `httplib2 0.12.1`
 * `requests 2.21.0`
2. Run `python3 database_setup.py`. This step will set up the database using SQLAlchemy.
3. Run `python3 db_init.py`. This step will create and populate the database with some initial categories, items and users. A new file will be created in your folder: `catalog.db`. For conviniance, I have already uploaded 
4. Run `python3 application.py`. This will start the application
5. Open your browser and type http://localhost:5000

hint: After a while playing around, you will have added, edited and deleted some new items. If you want to start using the original database, just delete the file `catalog.db` and run again `python3 db_init.py`.

## 4 Application ***Geek Coffee catalog*** 

* Use the GEEK COFFEE logo at top left corner to go to the main page.
* See the latest 10 items added to the catalog on the page center at the main page.
* Use the left menu to navigate through the existing categories.
* Once clicked in a category, the items of that category will show on the page center.
* Clicking on the item link will redirect you to the item's description.
* Use the top right corner button "Login" to be redirected to the login page
* At the login page, use Google to guarantee an authorization to the website. It is ok, this uses only an authentication method, it gives us no access to your Google account, password or private information. This action will create a user for you using the name and e-mail address only. Important: All the steps below can be only performed if you are logged in. Otherwise, you won't see the links, even if you try to type directly the URL (try hacking directly using, for example, this URL http://localhost:5000/catalog/additem ).
* Once logged in, you can create a new item on the main page clicking on the link _new item_ on the page center above _Latest items_
* If you go to a catalog category without any item added yet, you can also add new items using the link there.
* To edit or delete an item, go to its description page. The links to edit or delete the item are at the bottom right on the page center.
* To get a JSON endpoit access, use the following URL: http://localhost:5000/catalog.json
