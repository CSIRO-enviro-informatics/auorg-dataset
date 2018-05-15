# Minimal Flask MVC
This is a minimal Python3 Flask app that is structured along the lines of Model, View, Controller.

Its purpose is to act as a reference for Flask structure.

## Structure
Folders:  
* **model**
    * contains files to interface with data structures (databases/files etc.)
    * the files here are likely class files that get called by functions in controller
* **view**
    * contains template files, static files like CSS and other content used to formulate ouput formats
* **controller**
    * contains the declarations of Flask API endpoints - routes
    * these are the HTTP endpoints that, when accessed via a browser or some external agent trigger handling by this application
    * in this MVC formulation, the routes file(s) should be minimal and just respond to HTTP requests and hand off data access to model and use resources via views for responses
* **_config**
    * a basic config file to store things like pointers to static folders

Files:  
* **app.py**
    * the Flask application declaration
    * this can be run through a WSGI-capable web server, like Apache, by refering to it via the app.wsgi file
* **app.wsgi**
    * a file needed to be referred to by a web server, such as Apache, for some location, such as /app, so the web server can forward requests at that point to this Flask App
* **requirements.txt**
    * a listing of the Python modules required for this app

## Installation
To run this app using Apache2 web server on Debina/Ubuntu Linux:
* install Apache
	* sudo apt install -y apache2
	* sudo apt install apache2-utils
* enable Apache <--> Python3 interactions via mod_wsgi
	* sudo apt install libapache2-mod-wsgi-py3
	* sudo apt install python3-flask
* install Git in order to clone this repo
	* sudo apt install git
* clone the app somewhere
	* sudo mkdir /var/www/minimal
	* sudo chown -R ubuntu /var/www/minimal
	* cd /var/www/minimal
	* git clone https://github.com/nicholascar/minimal-flask-mvc.git .
* adjust this app's app.wsgi file to point to the dir you cloned it to
	* nano app.wsgi
* configure Apache to point to this app at /minimal
	* sudo nano /etc/apache2/sites-available/000-default.conf
	* add in the settings from the example apache.conf in this repo

## Contacts
**Nicholas Car**  
*Senior Experimental Scientist*  
CSIRO Land & Water  
Brisbane, Australia  
<nicholas.car@csiro.au>  
<http://orcid.org/0000-0002-8742-7730>  
