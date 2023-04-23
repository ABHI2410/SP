# Input Validation
## API that Validates name and phone number 


Programming Language: **Python 3.10**

Framework: **Django Rest Framework 3.14.0**

Master Branch Status: [![Build Status](https://app.travis-ci.com/ABHI2410/SP.svg?branch=master)](https://app.travis-ci.com/ABHI2410/SP)

### Steps to buid

- Using Docker

  `docker build -t <imagename> .`
  
  `docker run -it -p 8000:8000 <imagename>`
 
- Without Docker
 
  Install dependecies 
 
  `python3 -m pip install -r requirements.txt`
 
   Create Database
    
  `python3 manage.py makemigrations`
    
  `python3 manage.py migrate`
    
  Run the server
    
  `python3 manage.py runserver`

