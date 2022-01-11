# Project2-Distributed-Computing

## How to run service

To start it is necessary to have docker installed.

The first point are install all requeriments, for this move to the directory where the file requirements.txt is located

````
pip install -r requirements.txt
````
It is recomended using a virtual env.

Then in the docker-postgres directory run the command:
````
docker-compose up
````
this command start the postgres database

If it is the first time you run the first time you run the service, create all the tables in the database with the following commands:
````
flask db migrate
flask db upgrade
````

 And finally run the web service:
 ````
flask run --host=0.0.0.0
````
 

