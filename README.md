# Python/Flask todo with Docker

A simple todo application development environment using Docker and Docker Compose.

## Requirements

Support for Docker Compose version 3 (latest Docker Compose recommended)

_More may come..._

## Instructions

### Linux

```bash
# Go to repository folder
docker-compose up
```

Go to `http://localhost:8080/` when its finished loading.

To run in detached mode simply add the flag -d to the end of the command.

```bash
docker-compose up -d
```

Then kill the process with:

```bash
docker-compose kill
```

### Windows

Same as Linux.

If you run into an error while running docker-compose up, open the settings of Docker for Windows (right click icon in taskbar and select settings). Then go to Network tab and select Fixed DNS Server with the adress 8.8.8.8 (should be prefilled already). Apply and wait for docker to restart. Try docker-compose up again.

You also require a password in order to share files with docker, for some reason Docker can't handle a user without a password so if you don't have one, you should add a password to your profile.

### MacOS

Needed?

## Clean up

Instruction to clean up containers and images.

_**WARNING**_ Removes _all_ containers, images and volumes!

```bash
docker rm $(docker ps -a -q)
docker rmi $(docker images -a -q)
docker volume rm $(docker volume ls -f dangling=true -q)
```

## Robo 3T
[Robo 3T](https://robomongo.org/) (f.k.a. Robomongo) is a cross platform tool that allows you to view a mongo database and work directly with the data. This section explains how to connect Robo 3T with a mongoDB instance running in a docker container.

To connect the Robo 3T client to the mongoDB instance just open the program and connect to localhost:27017. You should then be able to connect and view the database inside the Robo 3T client.

## Links

* [Flask/MongoDB Tutorial](http://containertutorials.com/docker-compose/flask-mongo-compose.html)
* [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)


## API - Routes

#### Create Admin
http://nanotu.be/admins  | POST
Creates admin account with the credentials:

    username: admin
    password: admin123

Returns statuscode 201 and the JSON

    {
      "message": "Admin account has been created",
      "status": 201
    }


#### Authenticate Admin
http://nanotu.be/admins/auth | POST
Authenticates admin. Requires the following data:

    username: admin
    passowrd: admin123

Returns statuscode 200 and the JSON

    {
        "message": "Successfully logged in as admin",
        "status": 200,
        "token": "a-jwt-of-great-importance55"
    }

#### Get All Companies
http://nanotu.be/companies | GET
Gets a list of all companies

If ok: returns statuscode 200 and the JSON

    {
       "status": 200,
       "message": "Successfully extracted all companies",
       "companies": [
           {
               "username": "Company1"
            },
           {
               "username": "Company2"
            },
            ...
        ]
    }

If company name exists: returns 409 and the JSON

    {
       "message": "Company already exists",
       "status": 409
    }

#### Create Company
http://nanotu.be/companies | POST
Creates a company. Requires the following data:

    username: username-of-company
    password: password-for-company
    jwt: an-admin-jwt

If ok: returns statuscode 201 and the JSON

    {
       "message": "Company was created",
       "status": 201
    }

If company name exists: returns 409 and the JSON

    {
       "message": "Company already exists",
       "status": 409
    }

#### Authenticate Company
http://nanotu.be/admins/auth | POST
Authenticates company. Requires the following data:

    username: username-of-company
    password: password-for-company

Returns statuscode 200 and the JSON

    {
        "message": "Successfully logged in as company",
        "status": 200,
        "token": "a-jwt-of-great-importance42"
    }

#### Create Representative
http://nanotu.be/representatives | POST
Creates a representative. Requires the following data:

    username: name-of-representative
    password: password-for-representative
    jwt: a-company-jwt

If ok: returns statuscode 201 and the JSON

    {
       "message": "Representative was created",
       "status": 201
    }

If exists: returns 409 and the JSON

    {
       "message": "Representative already exists",
       "status": 409
    }

#### Authenticate Representative
http://nanotu.be/representatives/auth | POST
Authenticates representative. Requires the following data:

    username: representative-username
    password: representative-password

Returns statuscode 200 and the JSON

    {
        "message": "Successfully logged in as representative",
        "status": 200,
        "token": "a-jwt-of-great-importance33"
    }


