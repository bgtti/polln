<div align="center">
  <br>
  <h1><b>PollN</b></h1>
  <strong>helping ideas spread like pollen</strong> 
  <br>
  <strong>PRODUCTION VERSION</strong> 
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

**Live at [https://polln.bgtti.dev](https://polln.bgtti.dev)** 
\
**Video demo at [https://youtu.be/9yoCYDmnFfY](https://youtu.be/9yoCYDmnFfY)**

# Table of Contents
- [Introduction](#introduction)
   - [Installation](#installation)
   - [How PollN works](#how-polln-works)
   - [Branches: main and production](#branches-main-and-production)
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
- [Contributions](#contributions)
<br>
 
# Introduction
 PollN is an interactive presentation software for real-time audience engagement and feedback.
 Users can use PollN for live polling, quizzes, and surveys. The installation bellow is to be used with the main branch code. 

 **This is the code used in production, live at [pollN.bgtti.dev](https://polln.bgtti.dev/)**

 If you want to play around with this project, visit the [main branch](https://github.com/bgtti/polln/tree/main) for more information.

# Differences between main and production

The production branch is different from the main branch in the following way:

<details>
   <summary>1. Settings and requirements</summary>

   >\
   > Production (the `production` branch) requires some specific settings (prod_settings), while other are not relevant (dev_settings).
   > These two files (prod_settings and dev_settings) are not merged automatically.
   > Similarly, the `requirements.txt` is also never automatically merged, since this could cause issues in the production environment. 
   > Example: mysql-connector-python is used in production since mysqlclient lead to many errors. django-browser-reload id not useful in production environments, so it also removed from the requirements in the `production`branch.
   > Another file that is not merged directly is templates/django_reload.html - since it is connected to django-browser-reload and could cause errors in production.
   ><br/><br/>

</details>

<details>
   <summary>2. Procfile and runtime.txt</summary>

   >\
   > These files were added as per requirements of hosting in Railway.app, and as such, they only exist in the `production` branch. 
   > 
   ><br/><br/>

</details>

<details>
   <summary>3. mydb.py and .env.example</summary>

   >\
   > The content of mydb.py is only relevant for the db creation locally, and it is not needed in production. The file therefore only exists in `main` (or other branches).
   > Similarly, .env.example is only available in the `main` branch, since it is meant to be helpful to run this app locally.
   > 
   ><br/><br/>

</details>

# Pushing to production

The `production` branch is always kept up-to-date with the `main` branch.
Whenever the `main` branch is updated, the changes are merged into `production`.
A Github Workflow (*manual-merge-to-prod.yml*) sets some helpful rules so that certain files are ignored in the merge.
This means certain changes (such as to `requirements.txt`) need to be handled manually.

No direct contribution is possible to this branch.
If you would like to contribute to pollN, please fork and clone the `main` branch - and create any branches from that version. 