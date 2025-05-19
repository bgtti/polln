<div align="center">
  <br>
  <h1><b>PollN</b></h1>
  <strong>helping ideas spread like pollen</strong> 
</div>
<br>
<table align="center" style="border-collapse:separate;">
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent"><small>Python</small></td>
    <td style="background: #344955; border-radius:20px"><small>Django</small></td>
    <td style="background: #344955; border-radius:20px"><small>JavaScript</small></td>
    <td style="background: #344955; border-radius:20px"><small>MySQL</small></td>
    <td style="background: #344955; border-radius:20px"><small>Bootstrap</small></td>
    <td style="background: #344955; border-radius:20px"><small>Chart JS</small></td>
  </tr>
</table>
<hr>

![Preview of app](static/app_preview/PollN_preview_tablet_and_phone.gif)
<hr>

**Live at [https://polln.bgtti.dev](https://polln.bgtti.dev)**

**App video tour at [https://youtu.be/s2GuRkgv3cI](https://youtu.be/s2GuRkgv3cI)**

**Installation guide video vailable at [https://youtu.be/TvnNeX7b05s](https://youtu.be/TvnNeX7b05s)**

# Table of Contents
- [Introduction](#introduction)
   - [Installation](#installation)
      - [Local Set Up with MySQL locally](#local-set-up)
      - [Local Set Up with MySQL on docker](#local-set-up-with-mysql-on-docker)
      - [Run App with Docker](#run-app-with-docker)
   - [How PollN works](#how-polln-works)
- [Branches: main, production, etc](#branches-main-production-etc)
   - [main branch](#main-branch)
   - [main_dockerized branch](#main_dockerized-branch)
   - [production branch](#production-branch)
   - [version_1 branch](#version_1-branch)
   - [others](#others)
- [Code and organization](#code-and-organization)
   - [The project folder: polln](#the-project-folder-polln)
   - [The App folders: website, dashboard, present, and poll](#the-app-folders-website-dashboard-present-and-poll)
   - [The static folder](#the-static-folder)
   - [Templates](#templates)
   - [mydb.py](#mydb.py)
   - [env, gitignore, requirements](#env-gitignore-requirements)
   - [tests](#tests)
   - [Third-party code](#third-party-code)
- [About and license](#about-and-license)
- [Contribute](#contribute)
<br>
 
# Introduction
 PollN is an interactive presentation software for real-time audience engagement and feedback.
 Users can use PollN for live polling, quizzes, and surveys. The installation bellow is to be used with the main branch code. 

## Installation

You can run this project locally in three different ways:
1. Local Setup (App + MySQL): 
Run Django and MySQL directly on your machine.
See [local setup bellow](#local-set-up) 
2. Hybrid (App Locally + MySQL in Docker): 
Run the Django app locally, but use Docker for MySQL.
See [local setup with DB on docker section](#local-set-up-with-mysql-on-docker)
3. Fully Dockerized (App + MySQL): 
Run the entire stack in Docker.
See the [dockerized branch README](https://github.com/bgtti/polln/tree/main_dockerized) for more details

I have a video guide for the installation process in youtube, you can access [here](https://youtu.be/TvnNeX7b05s).
It covers the three different ways listed above.


### Local Set Up
<details>
   <summary>1. Clone this repository</summary>

   >\
   > Fork this repository, then clone into your fork.
   >
   > More information on how to clone this repository available at https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
   > It is recommended that you set up a virtual environment. More information: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#:~:text=To%20create%20a%20virtual%20environment,virtualenv%20in%20the%20below%20commands.&text=The%20second%20argument%20is%20the,project%20and%20call%20it%20env%20.
   > Use the main branch, which is intended for local (production). The code from the production branch was changed to suit the production environment. More information bellow.
   ><br/><br/>

</details>

<details>
   <summary>2. Create virtual env and install dependencies</summary>

   >\
   > Create a virtual environment:
   > ```pwsh
   >python -m venv env
   >```
   >
   >Then activate the environment with the following command:
   > ```pwsh
   >.\env\Scripts\activate
   >```
   >
   >Then proceed to install the requirements:
   >
   > ```pwsh
   >pip install -r requirements.txt
   >```
   > 
   > If you make changes to the project, you can always update the requirements with
   > 
   > ```pwsh
   >pip freeze > requirements.txt
   >```
   >
   > If you face issues with the installing the requirements: it is likely due to a couple of connector options.
   > Choose the one that works for you, and delete or uncomment the others:
   >
   > ```txt
   > mysql==0.0.3
   > mysql-connector-python==8.0.33 #=> This works for me
   > mysqlclient==2.1.1 #=> TDelete if it causes issues
   > # PyMySQL==1.0.3 #=> This is an option if the previous ones don't work
   > ```
   >
   ><br/><br/>

</details>

<details>
   <summary>3. Make sure you have mySQL installed</summary>

   >\
   > You can install mySQL here: https://dev.mysql.com/downloads/installer/
   > W3Schools has a great article on it: https://www.w3schools.com/mysql/mysql_install_windows.asp
   >
   >If you are new to mySQL with django, you might find this video helpful: https://www.youtube.com/watch?v=t10QcFx7d5k
   ><br/><br/>

</details>

<details>
   <summary>4. Create a .env file</summary>

   >\
   > In the root folder, you will see a file called `.env.example`.
   > Create a file names `.env`in the root folder and copy the contents of `.env.example` into it.
   > You should change at least one variable in this file:
   >
   > ```txt
   > MYSQL_USER = 'root' # <- the name of the user you set with MySQL, change if necessary
   > MYSQL_PASSWORD = 'your_MySQL_password_here' # <- you want to change this
   >```
   >
   > You want to use the same name and password you used to setup MySQL during installation.
   > 
   > More information about .env files (and python-dotenv ) here:
   > https://pypi.org/project/python-dotenv/
   ><br/><br/>

</details>

<details>
   <summary>5. Run the mydb.py file</summary>

   >\
   > Open the mydb.py file. This is the file that should create the database. Run the following terminal command:
   > ```python
   > python mydb.py
   >```
   >
   > <code>python manage.py migrate</code> initiates the database.
   > 
   > Run:
   > ```pwsh
   > python manage.py makemigrations website
   > python manage.py makemigrations dashboard
   > python manage.py migrate
   >```
   > 
   ><br/><br/>

</details>

<details>
   <summary>6. Create superuser and run the server</summary>

   >\
   > Create the superuser by typing the following in the terminal:
   > ```pwsh
   > python manage.py createsuperuser
   >```
   >
   > Set up a username, email, and password. Then start the server:
   > 
   > Run:
   > ```pwsh
   > python manage.py runserver
   >```
   > 
   ><br/><br/>

</details>

<br>
Open up your browser to see the homepage and start exploring.
<br><br>

![Preview of homepage](static/app_preview/PollN_preview_homepage.png)

### Local Set Up With MySQL on Docker

*What if I want to run MySQL on docker (instead of downloading MySQL)?*

You will want to follow the [local set up](#local-set-up):
1. Clone this repository
2. Create virtual env and install dependencies

and then:

3. Make sure you have docker installed 

<details>
   <summary>4. Create .env file</summary>

   >\
   > Create a .env file in the root folder and copy the content bellow:
   >
   > ```txt
   > DJANGO_SETTINGS_MODULE = 'polln.settings.dev_settings'
   >
   > SECRET_KEY = 'django-insecure-@b!g&8h80or2ebsau-qhqj(vc)lwkc99&cdiho6q(xyigwb0xo'
   > BASE_URL = 'http://127.0.0.1:8000'
   > ALLOWED_HOSTS = ''
   > CSRF_TRUSTED_ORIGINS = ''
   > 
   > MYSQL_ENGINE = 'django.db.backends.mysql'
   > MYSQL_NAME = 'pollndb'
   > MYSQL_USER = 'pollnuser'
   > MYSQL_HOST = '127.0.0.1'
   > MYSQL_PASSWORD = 'pollnpassword'
   > MYSQL_PORT = '3306'
   >```
   >
   ><br/><br/>

</details>

<details>
   <summary>5. Create a .yml file and compose</summary>

   >\
   > In the root folder, create a file named `docker-compose.yml` with the content:
   >
   > ```yml
   > services:
   >   db:
   >     image: mysql:8.0
   >     container_name: polln_mysql
   >     ports:
   >       - "3306:3306"
   >     environment:
   >       MYSQL_DATABASE: pollndb
   >       MYSQL_ROOT_PASSWORD: rootpassword
   >       MYSQL_USER: pollnuser
   >       MYSQL_PASSWORD: pollnpassword
   >     volumes:
   >       - mysql_data:/var/lib/mysql
   > 
   > volumes:
   >   mysql_data:
   >```
   >
   > Then run: 
   >```pwsh
   > docker-compose up -d
   >```
   ><br/><br/>

</details>

<details>
   <summary>6. Makemigrations, create superuser and run server </summary>

   >\
   > 
   > Run:
   > ```pwsh
   > python manage.py makemigrations website
   > python manage.py makemigrations dashboard
   > python manage.py migrate
   >```
   >
   > Create the superuser by typing the following in the terminal:
   > ```pwsh
   > python manage.py createsuperuser
   >```
   >
   > Set up a username, email, and password. Then start the server:
   > 
   > Run:
   > ```pwsh
   > python manage.py runserver
   >```
   > 
   > 
   ><br/><br/>

</details>

### Run App with Docker
If you want to run both the application as well as MySQL on docker, that is possible.
This way, you don't need to install the requirements nor MYSQL locally.

See the [dockerized branch README](https://github.com/bgtti/polln/tree/main_dockerized) for more details.

## How PollN works

The user must create an account, create a project and add at least one question to the project. The user will then be able to gather responses from one or more respondent in the following way:
<br>

1. **Live polling**:
The users can present the project and gather the answers live. The respondents will scan the QR code on the first page of the presentation, which will lead them to the project's questions. The users can see how many responses were received. When the users move on to the second presentation slide, the poll will be closed. The next prosentation slides will be an analysis of the gathered questions.

2. **Sending the poll link**:
The user can open the poll and send the link to the project per email, WhatsApp or any preferred mean. The user can close the poll to see the results in table-format. The users can download the results in excel (csv), and re-open the poll to gether the next set of answers should they want to.
<br>

The users can ask three type of questions: open-ended, question and answer (Q&A), or multiple-choice.
The questions of type Q&A must have a correct answer, and multiple-choice may or may not have a correct answer. The user can also control the order in which questions appear in a poll by dragging elements into the desired position.

Users can allow for anonymous answers or request a password to access the poll. They may also choose if they want the respondents to see the answers (to questions where a correct answer was given) after they submitted their answers.

Respondents can access the poll in 3 different ways: scanning the QR code with their phones (during a presentation), via the poll link, or inputting the poll code in the specified field on the homepage. Polls can only be accesed when they are open. 

The user can close a poll any time. Poll opening and closing will happen automatically during a presentation. Polls can also get closed when the user makes changes to the structure of the project, such as adding/editting questions, editting the project, or changing the question order.

A full guide on how to use PollN is provided in the url `/guide`.
<br><br>

# Branches: main, production, etc

## main branch
Up-to-date branch, use to run the code and MySQL locally (MySQL should be installed).
You can set up a virtual environment and install the dependencies to run.
You can optionally run MySQL in docker and delete the `mydb.py` file.

## main_dockerized branch
If you want to run the app on docker instead of installing dependencies, use main_dockerized

## production branch
Contains the PollN code deployed at https://polln.bgtti.dev .

## version_1 branch
Contains the original code written in 2023. 
This version was submitted as the final project for HarvardX's course CS50w.
It is featured in a video demo [available here](https://youtu.be/9yoCYDmnFfY).

## others
Any other branch that you may find in this repo is a development branch and should be ignored.

# Code and organization
The polln application has the following structure:
- It is divided into 4 apps: website, dashboard, present, and poll
- Each app folder contains a views.py and templates folder. Views might import from a utils.py.
- Only two apps have db models in models.py: website and dashboard
- The static folder is a standalone. All css and JS files, as well as media are there
- A standalone templates folder contain shared templates only.
- Each app also contains a tests.py file.

Let's take a look at what each app does.
<br>

## The project folder: polln
<br>
The polln folder is the standard django application folder. It contains the settings module, which contain environment-specific configurations. If you clone the main branch, you may delete the prod_settings.py as it is not relevant for local development purposes and it will not impact the running of the application.
<br><br>

## The App folders: website, dashboard, present, and poll

### **1. website**
Contains the files responsible for the homepage, guide page, sign-up, and log-in. It is responsible for the creation and deletion of user accounts.
### **2. dashboard**
Contains most of PollN's logic. This is where projects and questions get added, deleted, or modified. It contains the 'My Projects'/'Dashboard' views, project pages, and the result's page. A utils.py file also contains helpful functions used by it's views.py file, but also in the views file of other apps.
### **3. presentation**
Contains the logic needed for the user to present and gather the responses in live polling. It will make requests to check the number of responses comming in to show on the presentation page, and make use of chart JS to display the results of multiple-choice questions, for instance.
### **4. poll**
Will check if the respondent has access to the poll, check if the poll is open, and gather poll results. It is responsible for the way the project is viewed by respondents. 

## The static folder
Shared styling is under common.cs, while shared JS functions are in main.js.
Styling and JS logic, as well as media files (pictures, videos, icons) are organized into subfolders named after the app using them. Website, dashboard, present, and poll have their own static folder here. the app_preview folder contains media used in this readme.md while favicon_io is the folder containing the favicon for this application.

Classes were named after their origin. For instance, the class 'BASE-hide' (or any class starting with 'BASE') will be in the common.css file. Any class starting with 'DASHBOARD-...' will be styled in the dashboard css file, and so on. Bootstrap was also used.

<br>

## Templates
Each app counts with its own templates folder. The standalone 'templates' folder contains the html files shared by 2 or more apps.
<br>

## mydb.py
This file is only to be used for the database creation. PollN uses mySQL. Check the installation instructions for more information. This file is not needed if you are running MySQL in Docker.
<br>

## env, gitignore, requirements
As noted in the installation instructions, an .env file (and a .gitignore so that the env is not pushed to git) was created to save the mySQL database password. You can use this app by adding your own mySQL password to the settings.py file in the polln folder.

The requirements.txt hold dependencies such as dotenv and mysql-connector-python.
<br>

## tests
As noted before, each app contains a tests.py file.
To run all tests, use the following command from the root folder: 
```pwsh
   python manage.py test
```
<br>

## Third-party code
Writing the codebase required some research. Source for media such as icons are included in the code. In comments you will also see helpful sources for styling (for instance, border-boxes), and links to helpful content that made this project possible. Some functions that were written by other authors or based on someone else's logic are clearly described as such and contain the original source link and author (when available).

Some special mentions:

- To enable drag and drop on mobile devices, I used the DragDropTouch polyfill from Bernardo-Castilho. More information [here](https://github.com/Bernardo-Castilho/dragdroptouch)
- The library qrcode.js was used for the code generation:  [qrcode](https://davidshimjs.github.io/qrcodejs/)
- Chart JS was used to create the bar chart: [chartJS](https://www.chartjs.org/)
- Damjan Pavlica made swipe effects on the presentation possible with this [StackOverflow answer](https://stackoverflow.com/a/56663695/14517941)
- Kyle from Web Dev Simplified wrote the question drag&drop login in [a video](https://www.youtube.com/watch?v=jfYWwQrtzzY&t=655s
)

# About and license

This project was originally created in 2023 as the [capstone project](https://cs50.harvard.edu/web/2020/projects/final/capstone/) for CS50w from HarvardX. The original (submitted version) can still be found in the branch `version_1`.Since then, more than a couple of bugs have been fixed.

This is a personal project completed by the author, which you are welcome to use and modify at your discretion. (MIT Licence)

PollN is a free open-source software that makes no claims as to its quality or reliability. The creator shall not be liable for any damage, loss of profit, revenue, or data incurred by you or any third-party arising from the access of or content created through the use of this site.

If you liked this project, motivate the developer by giving it a :star: on Github!

<br>

# Contribute

PollN featured in an article by Hazem Abbas in 2023 ["15 Open-source Free Self-hosted Survey, Poll Generators and Vote Management Solutions"](https://medevel.com/15-poll-generator/)!

**You can help make PollN a great software by contributing to this project!**

How to contribute:
1. Fork the repository: Click the "Fork" button at the top right of this page
2. Clone your fork locally
3. Create a new branch from `main`, naming it with the new feature or bug fix:  `git checkout -b your-feature-name`
4. Make your changes
5. Make sure the tests still pass (or write test if necessary)
6. Push to your fork
7. Create a Pull Request

Guidelines:
- Write tests for any new functionality
- Stick to existing coding conventions
- Keep commits focused and meaningful
- Before creating a pull request, make sure you are up-to-date with upstream (`git pull`) and solve any conflicts.
- Make sure your branch was created from `main` (and not other branches)
