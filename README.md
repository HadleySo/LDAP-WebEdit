# LDAP-WebEdit

Web based GUI LDAP editor for Cisco SPA LDAP.  


A Flask application to edit remote LDAP phonebook entries.

There are three functions:
- Add
- Delete
- Search

The LDAP entry fields are designed for Cisco corporate phonebooks on OpenLDAP. Connections to the LDAP server are established when the user has submitted a valid request and is taken down as soon as the server responds.
Authentication is only done during add and delete functions, otherwise LDAP is queried on an anonymous connection. A simple DN + Password authentication is used.

----

<details>
    <summary>Installation on Raspberry Pi</summary>

<br>
  
- Install Apache2 
- Install Python VENV ```sudo apt install python3-venv```
- In ```/var/www/``` create a directory for the Flask app. For example use ```mkdir``` to make ```/var/www/LDAP-web-app```
<br>

- Create a venv with ```sudo python3 -m venv venv``` and grant yourself permission with ```sudo chown -R pi:pi venv```
- Activate the venv with ```. venv/bin/activate```
- In the venv, install requirements ```pip install -r requirements.txt```
<br>

- Put the repository files into ```/var/www/LDAP-web-app```
- Make a ```logs/``` directory inside ```/var/www/LDAP-web-app```
- Grant apache2 rights with ```sudo chgrp -R www-data LDAP-web-app/```
<br>

- Install ```sudo apt install libapache2-mod-wsgi-py3```
- Create an apache2 config file ```sudo nano /etc/apache2/sites-available/LDAP-app.conf```
```
<VirtualHost *:80>
    ServerName yourDOMAINhere.com
    WSGIDaemonProcess LEdit user=www-data group=www-data threads=5 python-home=/var/www/LDAP-web-app/venv python-path=/var/www/LDAP-web-app
    WSGIScriptAlias / /var/www/LDAP-web-app/LDAP-app.wsgi

    <Directory /var/www/LDAP-web-app>
        WSGIProcessGroup LEdit
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
	Allow from all
    </Directory>
	
    ErrorLog /var/www/LDAP-web-app/logs/error.log
</VirtualHost>
```
- Enable the config file ```sudo a2ensite LDAP-app.conf```
<br>

- Create a wsgi file in ```sudo nano /var/www/LDAP-web-app/LDAP-app.wsgi```
```
#! /usr/bin/python3.7.3

from LEdit import app as application
```

- Restart the apache2 service ```sudo service apache2 restart```
  
</details>
