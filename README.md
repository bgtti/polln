<div align="center">
  <br>
  <h1><b>PollN</b></h1>
  <strong>helping ideas spread like pollen</strong> 
  <br>
  <strong>DOCKERIZED VERSION</strong> 
</div>
<br>
<table align="center" style="border-collapse:separate;">
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent"><small>Python</small></td>
    <td style="background: #344955; border-radius:20px"><small>Django</small></td>
    <td style="background: #344955; border-radius:20px"><small>JavaScript</small></td>
    <td style="background: #344955; border-radius:20px"><small>mySQL</small></td>
    <td style="background: #344955; border-radius:20px"><small>Bootstrap</small></td>
    <td style="background: #344955; border-radius:20px"><small>Chart JS</small></td>
  </tr>
</table>
<hr>

![Preview of app](static/app_preview/PollN_preview_tablet_and_phone.gif)
<hr>



**This branch contains the required files to run this application on docker.**

Requirements: have docker installed.

You do not need to have MySQL installed to run this branch.

# Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [About this branch](#about-this-branch)
   - [Working with this branch](#working-with-this-branch)
- [Support This Project](#support-this-project)

<br>
 
# Introduction
 PollN is an interactive presentation software for real-time audience engagement and feedback.
 Users can use PollN for live polling, quizzes, and surveys. 

 The installation bellow refers to this branch.
 
# Installation

<details>
   <summary>1. Fork & Clone this repository & Choose this branch</summary>

   >\
   > Fork this repository, then clone your fork:
   >
   > ```pwsh
   > git clone https://github.com/YOUR-USERNAME/pollN.git
   > cd pollN
   > git checkout main_dockarized
   >```
   >
   ><br/><br/>

</details>

<details>
   <summary>2. Make sure docker is installed</summary>

   >\
   > You’ll need Docker installed. If you don’t have it yet, get it here:
   > 👉 https://www.docker.com/get-started
   >
   > f you have a local MySQL instance running, please stop it —
the container needs to bind to port `3306`.
   > 
   ><br/><br/>

</details>

<details>
   <summary>3. Add a .env</summary>

   >\
   > Create a .env file in the root folder.
   > Copy the contents of the file `.env.docker.example` into it and save.
   >
   > ```pwsh
   > cp .env.docker.example .env
   >```
   ><br/><br/>

</details>

<details>
   <summary>4. Build and run the app</summary>

   >\
   > Make sure docker is running.
   >
   > Run the following to build and start the app:
   >
   > ```pwsh
   > docker-compose up --build
   >```
   >
   > This will: start the django app, start a MySQL database, Run database migrations, collect static files, and start the server with Gunicorn.
   >
   ><br/><br/>

</details>

<details>
   <summary>5. Create a Django superuser</summary>

   >\
   > Open a new terminal (in the same directory) and run:
   >
   > ```pwsh
   > docker-compose exec web python manage.py createsuperuser
   >```
   >
   > Follow the prompts to enter: a username, an email (optional), a password.
   >
   > Your superuser will now be able to log into /admin.
   ><br/><br/>

</details>

<details>
   <summary>6. Access the application</summary>

   >\
   > The app will be running at:
   > http://localhost:8000
   >
   > Using your superuser credentials, you will be able to log into http://localhost:8000/admin.
   > 
   ><br/><br/>

</details>

<br>
Open up your browser to see the homepage and start exploring.
<br><br>

## Dockerhub Image
If you encounter any issues building the image locally, a prebuilt version is available on Docker Hub:

👉 [Docker Hub - bgtti/polln](https://hub.docker.com/r/bgtti/polln)

Pull it with:

```pwsh
   docker pull bgtti/polln
```
You can then run it like this:

```pwsh
   docker run --env-file .env -p 8000:8000 bgtti/polln
```

💡 Make sure you have a `.env` file ready — use `.env.docker.example` from the `main_dockerized` branch as a template.

# About this branch

This branch differs from main in the following ways:

1. **.dockeringore**:
Makes sure some files are ignored when the container is built.

2. **.env.docker.example**:
This example env file differs from the .env.example available in the `main` branch. 

3. **docker-compose.yml**:
Defines the multi-container application.

4. **Dockerfile**:
Outlines the steps to create the containerized application environment.

5. **entrypoint.sh**:
Configures the executables that will run after the container is initiated.

6. **requirements.txt**:
Some requirements were commented out, so this file is not exactly the same as the one in the `main` branch.
Specifically: only the `mysql-connector-python` is needed, as the other connectors would not be suitable for this branch.
The following requirements were removed: mysql==0.0.3, mysqlclient==2.1.1, and PyMySQL==1.0.3.

7. **mydb.py**:
This branch runs MySQL on docker, so this file was removed in this branch.
It is required in the `main` branch to create the db locally.

## Working with this branch

Working with this branch offers some benefits:
💡 No virtual environment needed!
💡 No local MySQL needed!

If you make changes to the source code, changes are instantly reflected.
💡 Just restart the container (or even sometimes just reload the browser), no need to rebuild, just refresh the browser.

When you need to rebuild the container:
- If you change the Dockerfile
- Add/change requirements.txt
- Change the Python version or install system/Python packages

```pwsh
   docker-compose up --build
```

Will data persist between runs?
Yes, volumes are set.
So will the data persist if you run certain docker commends?
```pwsh
   docker-compose stop # yes
   docker-compose down # yes
   docker-compose down --volumes # no
```

# Support This Project

If you liked this project, consider giving it a ⭐ on GitHub — it motivates the developer and helps others discover it!