**PROJECT DESCRIPTION**
    In this basically we are building the api's (CRUD) using django rest framewrok and django orm as (ORM) and using the SQL database (sqllite3).
    Audio file type can be one of the following:
    1 – Song
    2 – Podcast
    3 – Audiobook

**Song file fields:**
    - ID – (mandatory, integer, unique)
    - Name of the song – (mandatory, string, cannot be larger than 100
    characters)
    - Duration in number of seconds – (mandatory, integer, positive)
    - Uploaded time – (mandatory, Datetime, cannot be in the past)

**Podcast file fields:***
    - ID – (mandatory, integer, unique)
    - Name of the podcast – (mandatory, string, cannot be larger than 100
    characters)
    - Duration in number of seconds – (mandatory, integer, positive)
    - Uploaded time – (mandatory, Datetime, cannot be in the past)
    - Host – (mandatory, string, cannot be larger than 100 characters)
    - Participants – (optional, list of strings, each string cannot be larger than
    100 characters, maximum of 10 participants possible)

**Audiobook file fields:**
    - ID – (mandatory, integer, unique)
    - Title of the audiobook – (mandatory, string, cannot be larger than 100
    characters)
    - Author of the title (mandatory, string, cannot be larger than 100
    characters)
    - Narrator - (mandatory, string, cannot be larger than 100 characters)
    - Duration in number of seconds – (mandatory, integer, positive)
    - Uploaded time – (mandatory, Datetime, cannot be in the past)


**Note**
    we created only four endpoints (Generic and usable for all audio file types)
    - in this project the Postman Collection is also attached and cover the edge cases also

**Pre-requisite**

    We Assume that you already have python3 in your system.
    This project supports django-3.0 version.

**Requirements** 

    The requirements that is there in the requirements.txt file.
    Please run the following command in the project directory.

    pip3 install -r requirements.txt

**Instruction**

    To run the code in your device please follow the below intructions:-
    1.To create virtual environment, run the command: python3 -m venv <name of vitual env>
    2.To activate the enviroment, run the command: source <name of your virtual env>/bin/activate 
    3.To install the requirements run the command: pip3 install -r requirements.txt
    4.To migrate the data from database run:python3 manage.py makemigrations and python3 manage.py migrate
    5.To run the server use the command: python3 manage.py runserver (in project root directory)