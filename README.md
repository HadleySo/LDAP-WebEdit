# LDAP-WebEdit

Web based GUI LDAP editor for Cisco SPA LDAP.  


A Flask application to edit remote LDAP phonebook entries.

There are three functions:
- Add
- Delete
- Search

The LDAP entry fields are designed for Cisco corporate phonebooks on OpenLDAP. Connections to the LDAP server are established when the user has submitted a valid request and is taken down as soon as the server responds.
Authentication is only done during add and delete functions, otherwise LDAP is queried on an anonymous connection. A simple DN + Password authentication is used.
