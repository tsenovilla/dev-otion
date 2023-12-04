# Description

Have you ever spent many hours of your programming time trying to solve a specific problem? I'm sure you've had to gather information obtained from several sources until you found all the tools required for your particular need. Dev-otion has born in order to help people with this kind of problems. It's a web-blog where I will be posting interesting information about programming, including all the problems I'll face in my own way, where the solution implies a few hours of research. You can find dev-otion at https://dev-otion.com and this repo contains its source code.

The project's backend is built using **Django**, while the frontend is composed by **SCSS** and **JS**. In development environment, we use **Gulp.js** as a task runner in order to improve the performance of static images, bundle scripts and compile the **SCSS** into **CSS** stylesheets.

## Usage

This project is about coding, about overcoming difficulties in programming. Maybe you're interested in running it locally and play with it, maybe you are building a website sharing some features with Dev-otion and the code may help you. Thus, you can clone this repo and modify whatever you like in your own computer, feel free! You can do whatever you like provided that you do not violate the copyright or make profits with a copy of it.

The code runs in both environments, development and production. The production code is thought to be hosted as a DigitalOcean App, using DigitalOcean Spaces to hold static and media fields (if you are trying to deploy it in another server, you'll have to modify it accordingly). 

In order to make the project work correctly in a localhost, there's a few steps that you must follow:

1. If you are running a local clone, create a virtual environment using `Python 3.11.3` and run `pip install -r requirements.txt` to install all the Python development dependencies. 

2. Run `npm install` to install the node dependencies needed for development. Then, run `npm run build_static` to build all the static fields from the `src` folder. Now you can use the following commands when developing:

    - `npm run compile_css`: To compile all the **SCSS** files from the `src` folder into a single **CSS** stylesheet.
    - `npm run export_js`: To bundle all the **JS** files from the `src` folder with the imported libraries into a single script.
    - `npm run dev`: If you run this command, each time a **SCSS** or **JS** file is modified, `compile_css` or `export_js` is run.
    - `npm run improve_images`: To improve the quality and the web performance for the images, getting also an AVIF and WebP version.

3. Create a `.env` file where you will assign your environment variables. You must include:

    - `DB_HOST`: The host name where your MySQL database is located (as it is local, it will probably be 127.0.0.1)
    - `DB_NAME`: Your database name
    - `DB_USER`: Your database user
    - `DB_PASS`: Your database password
    - `BREVO_API_KEY`: This API key is used to send emails through Brevo. You can obtain it if you create an account in Brevo and register a project. If you are not using the e-mail feature for your purposes, this variable is not really needed.

4. Run `python manage.py makemigrations` and `python manage.py migrate` to setup the database. You can also run `python manage.py createsuperuser` to create an admin user, so you can explore also the admin site.

5. Run `python manage.py compilemessages` to create the language files, so the blog may be read in the configured languages.

If you are trying to deploy the project to a real server, the requirements change a bit, so use `prod_requirements.txt` in step 1 (DigitalOceanApps uses **PostreSQL**, so the database binding installed will be `psycopg2`. Keep this in mind if you need another one). You do not need the `src` files and the Node modules anymore (if you have run `npm run build_static`), so just delete them. The environment variables change in a real server, the only one that remains is `BREVO_API_KEY`, but you'll have to add `DATABASE_URL`,`SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` (corresponding to the URL pointing to your database created by your server provider, the Django secret sey, and the hosts allowed to run the app, respectively). If you are using DigitalOcean Spaces to hold static/media files, you must set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as well, otherwise modify the script `django_config/settings.py` accordingly and add the environment variables you need.

#### Note

After updating my OS, I've noticed that the development configuration isn't work anymore in my computer due to a problem with the mysqlclient binding in Django. It's not harmful in production as it's deployed on DigitalOcean and there PostgreSQL is used (I've choosen MySQL at the creation time without knowing that I was going to use PostgreSQL in production, don't change it afterwards because the functionality doesn't change and I have all the tables already created in MySQL in my localhost). If you create your tables directly with PostgreSQL in your localhost it's OK, otherwise, keep reading this note. 

I've found out that this problem is kind of usual with Django and mysqlclient (eg, [check this](https://stackoverflow.com/questions/46902357/error-loading-mysqldb-module-did-you-install-mysqlclient-or-mysql-python)), but I've not discovered why that's happening although it seems to be a problem with some dependencies. The solution proposed in the link involving pymysql made the thing for my localhost though I read that it doesn't work for other people. I'm leaving this note here in the case you face such a problem, you'll have at least a starting point to investigate :)

Other
=====

Author: Tomás Senovilla Polo

Email : tspscgs@gmail.com
