# PollN
 PollN is an interactive presentation software for real-time audience engagement and feedback.

![Preview of app](static/app_preview/PollN_preview_tablet_and_phone.gif)

## Installation

<details>
   <summary>1. Clone this repository</summary>

   >\
   > More information on how to clone this repository available at https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
   ><br/><br/>

</details>

<details>
   <summary>2. Install dependencies</summary>

   >\
   > ```pwsh
   >pip install -r requirements.txt
   >```
   > 
   > If you make changes to the project, you can always update the requirements with
   > 
   > ```pwsh
   >pip freeze > requirements.txt
   >```
   ><br/><br/>

</details>

<details>
   <summary>3. Make sure you have mySQL installed</summary>

   >\
   > You can install mySQL here: https://dev.mysql.com/downloads/installer/
   > W3Schools has a great article on it: https://www.w3schools.com/mysql/mysql_install_windows.asp
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
   <summary>4. Change the DB password</summary>

   >\
   > Go to the PollN folder and open the settings.py file
   > ```python
   > DATABASES = {
   >    'default': {
   >    'ENGINE': 'django.db.backends.mysql',
   >    'NAME': 'pollnmysql',
   >    'USER': 'root',
   >    'PASSWORD': os.environ.get('MY_SQL_ROOT_PASSWORD'), # Your password here
   >    'HOST': 'localhost',  
   >    'PORT': '3306',
   >     }
   > }
   >```
   >
   > Alternatively, you can create an .env file in the main folder, then create the variable 'MY_SQL_ROOT_PASSWORD'='your_password_here'
   > 
   > python-dotenv should be a dependency already. More information here:
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

<br/><br/>
Open up your browser to see the homepage and start exploring.

![Preview of homepage](static/app_preview/PollN_preview_homepage.png)

## How PollN works



1. **Website**





## Planning/ requirements/ brainstorming

The idea what PollN should be:
PollN  is an interactive software platform that enables users to engage audiences, gather feedback, and conduct real-time polls, quizzes, and surveys.
Key words: live polling, audience engagement platform

Name: poll n nr of people -- spread questions like pollen

- create questions
- get audience response
- get instant feedback

Drag and drop functionality
To enable drag and drop on mobile devices, I used the DragDropTouch polyfill from Bernardo-Castilho. More information at https://github.com/Bernardo-Castilho/dragdroptouch

QR code
a QR code is generated that can be scaned by poll repondants and links to the poll pagae.
The library qrcode was used for the code generation:  https://pypi.org/project/qrcode/
the helper function in dashboard/utils generating the link must have the base url changed if deployed


## Distinctiveness and Complexity
This project was submitted as the capstone project for CS50w. This Django-vanilla-JavaScript project is very distinct in nature than the projects from the lessons and from other final projects submitted by students - where a live polling app could not be found up to the date of writing (June 6, 2023).
PollN is also more complex in that it involved the creation of four inter-connected django apps holding multiple template and styling files, communication from back- and front-end via JSON files, interactive interface with animations, the use of the MySQL database, and changes in the Settings.py beyond what was covered in the course. 

More information about the CS50w requirements available at https://cs50.harvard.edu/web/2020/projects/final/capstone/

If you liked this project, motivate the developer by gifing it a :star: on Github!