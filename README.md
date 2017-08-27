# Directory -- A RESTful API Exercise


## Overview
----
This (somewhat poorly) named project demonstrates a RESTful API, written in 
Python and using the django framework.

Entries are made through GET, PUT, POST and DELETE calls to the endpoint.
The data comes in the form of key-value pairs; no particular judgement is
being made about the content, but it was originally planned to store addresses
for particular names, like an address book or directory -- hence the name.

It has not been deployed anywhere, so using it necessitates calls to localhost.
So, for example:  
`http://localhost:8000/addresses/?api=1&name=Eric` 
will return all of the entries for 'Eric' in a JSON, which might look like this:
`{"Eric": ["example@gmail.com", "example@hotmail.com, example@yahoo.com"]}`
(This is true if such addresses have already been posted to the endpoint.)

These are the possible fields for calls to the endpoint:
* 'api' (so far, only version 1 is being used, so this must =1)
* 'name'
* 'adddress'

If the GET call does not have the 'name' field set then all entries in the
database are returned.
PUT, POST, and DELETE calls look similar and need to have all of the 
fields filled out.


## Operation
----

Web Site serving is done through Django's standard process:

`$ python manage.py runserver`

The website landing-page should be subsequently available at:
` http://127.0.0.1:8000/addresses`
 
 
 Postman (https://www.getpostman.com/) has been used to validate this API.
 Here is a sequence of commands to demonstrate how it operates, presuming
 the database is empty to start with:
 ```
 command:  GET  http://localhost:8000/addresses/?api=1
 response:  {}  200 OK
 command:  POST http://127.0.0.1:8000/addresses/?api=1&name=Eric&address=example@gmail.com
 response:  200 OK
 command:  GET  http://localhost:8000/addresses/?api=1
 response:  {"Eric": ["example.gmail.com"]}  200 OK
 command:  POST http://127.0.0.1:8000/addresses/?api=1&name=Eric&address=example@yahoo.com
 response:  200 OK
 command:  GET  http://localhost:8000/addresses/?api=1
 response:  {"Eric": ["example@gmail.com", "example@yahoo.com"]}  200 OK
 command:  POST http://127.0.0.1:8000/addresses/?api=1&name=Eric&address=example@yahoo.com
 response:  403 Forbidden
 command:  PUT  http://127.0.0.1:8000/addresses/?api=1&name=Eric&address=example@yahoo.com
 response:  200 OK
 command:  PUT  http://127.0.0.1:8000/addresses/?api=1&name=Eric&address=example@hotmail.com
 response:  404 Not Found
 command:  DELETE  http://127.0.0.1:8000/addresses/?api=1&name=Eric&address=example@hotmail.com
 response:  404 Not Found
 command:  DELETE  http://127.0.0.1:8000/addresses/?api=1&name=Eric&address=example@gmail.com
 response:  204 No Content
 command:  POST http://127.0.0.1:8000/addresses/?api=1&name=Bob&address=bob@example.com
 response:  200 OK
 command:  GET  http://localhost:8000/addresses/?api=1
 response:  {"Eric": ["example@yahoo.com"], "Bob": ["bob@example.com"]}  200 OK
 command:  GET  http://localhost:8000/addresses/?api=1&name=Bob
 response:  {"Bob": ["bob@example.com"]}  200 OK
 ```
 

### Installation And Run Steps:

Clone the repository.  It will provide the code to run:

`$ git clone https://github.com/echase6/Directory`

Install necessary modules:

`$ pip install -r requirements.txt`

Create the db.sqlite3 file, but with no useful data:

`$ python manage.py migrate`

Create a superuser account, which might come in handy later:

`$ python manage.py createsuperuser`

Start the server:

`$ python manage.py runserver`

Then use a tool to send GET/PUT/POST/DELETE requests to the endpoint.

Enjoy!


