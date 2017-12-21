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
https://nanotu.be/admins  | POST
Creates admin account with the credentials:

    username: admin
    password: admin123

Returns statuscode 201 and the JSON

    {
      "message": "Admin account has been created",
      "status": 201
    }


#### Authenticate Admin
https://nanotu.be/admins/auth | POST
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
https://nanotu.be/companies | GET
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
https://nanotu.be/companies | POST
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
https://nanotu.be/auth | POST
Authenticates company. Requires the following data:

    username: username-of-company
    password: password-for-company

Returns statuscode 200 and the JSON

    {
        "message": "Successfully logged in as company",
        "status": 200,
        "token": "a-jwt-of-great-importance42"
    }


#### Get All Representatives
https://nanotu.be/companies/{company-name}/representatives | GET
Gets all representatives from specific company.

Returns statuscode 200 and the JSON

    {
      "message": "Successfully extracted all representatives for {company-name}",
      "representatives": [
        {
            "username": "adminsasdasd"
        },
        {
            "username": "one"
        }
      ],
      "status": 200
    }

#### Create Representative
https://nanotu.be/companies/{company-name}/representatives | POST
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
https://nanotu.be/auth | POST
Authenticates representative. Requires the following data:

    username: representative-username
    password: representative-password

Returns statuscode 200 and the JSON

    {
        "message": "Successfully logged in as representative",
        "status": 200,
        "token": "a-jwt-of-great-importance33"
    }

#### Create Consumer
https://nanotu.be/consumers | POST
Creates a consumer. Requires the following data:

    username: name-of-consumer
    password: password-for-consumer

If ok: returns statuscode 201 and the JSON

    {
       "message": "User was created",
       "status": 201
    }

If exists: returns 409 and the JSON

    {
       "message": "User already exists",
       "status": 409
    }

#### Authenticate Consumer
https://nanotu.be/auth | POST
Authenticates consumer. Requires the following data:

    username: consumer-username
    password: consumer-password

Returns statuscode 200 and the JSON

    {
        "message": "Successfully logged in as consumer",
        "status": 200,
        "token": "a-jwt-of-great-importance33"
    }

#### Get Categories
https://nanotu.be/categories | GET
Gets all available categories.

    "message": [
        {
            "category": "toaster",
            "_id": 0
        },
        {
            "category": "not-toaster",
            "_id": 1
        }
    ],
    "status": 200

#### Create Category
https://nanotu.be/categories | POST
Creates a new category. Requires the following data:

    "jwt": "an.admin.jwt",
    "category": "new-category-name"

Returns statuscode 201 and the JSON

    {
        "message": "Category created",
        "status": 201
    }

#### Create Subcategory
https://nanotu.be/categories/<parent-category>/subcategories | POST
Creates a new sub-category. requires the following data:

    "jwt": "ad.admin.jwt",
    "category": "new-sub-category-name"

Returns statuscode 201 and the JSON

    {
        "message": "Subcategory created",
        "status": 201
    }

#### Get products
https://nanotu.be/products | GET
Gets all products in the system.

Returns statuscode 200 and the JSON

    {
        "message": "Successfully retreived all the products",
        "status": 200,
        "data": {
            "products": [
                {
                    "_id": "5a201042e3214800071cf307",
                    "category": "cars",
                    "createdBy": "ElonMusk",
                    "description": "en gul bil",
                    "files": [
                        {
                            "file": "/materials/tesla/productID/filename-15120535634336069.pdf"
                        }
                    ],
                    "name": "gul bil",
                    "producer": "tesla"
                }
            ]
        }
    }

#### Create product
https://nanotu.be/products | POST
Creates a new product. Requires the following data:

    "jwt": "a.representative.jwt",
    "name": "product.name",
    "productNo": "product.serial.number",
    "description": "product.description",
    "category": "product.category",
    "files": [] //optional array of files

Returns the following JSON:

    {
        "data": {
            "product": {
                "_id": "5a2025d4e32148031032e9d4",
                "category": "cars",
                "createdBy": "ElonMusk",
                "description": "en blå bil",
                "files": [], //If no files were present in the POST request
                "name": "blå bil",
                "producer": "tesla",
                "productNo": "122"
            }
        },
        "message": "Product was created",
        "status": 201
    }

#### Upload material to product
https://nanotu.be/products/<_id>/materials | POST
Uploads material to the specified product Requires the following data:

    "jwt": "a.representative.jwt",
    "files": [pdf.files.to.upload]

Returns the following JSON:

    {
        "data": {
            "product": {
                "_id": "5a202ddfe3214803f7dc192a",
                "category": "cars",
                "createdBy": "ElonMusk",
                "description": "en blå bil",
                "files": [
                    {
                        "file": "/materials/tesla/product_id/filename-1512058335748237.pdf"
                    },
                    {
                        "file": "/materials/tesla/product_id/filename-15120583750399292.pdf"
                    },
                    {
                        "file": "/materials/tesla/product_id/filename-15120583750524912.pdf"
                    },
                    {
                        "file": "/materials/tesla/product_id/filename-15120583750654202.pdf"
                    }
                ],
                "name": "blå bil",
                "producer": "tesla",
                "productNo": "1223"
            }
        },
        "message": "Successfully uploaded material to the product",
        "status": 200
    }


#### Get product info
https://nanotu.be/products/<_id> | GET
Gets the information for the specified product. Returns the following JSON:

   {
        "data": {
            "product": {
                "category": "Mon Dec 04 2017 17:05:05 GMT+0100 (CET)",
                "createdBy": "889748890",
                "files": [
                    {
                        "average": 5,
                        "comments": [],
                        "material_id": "hej-15125582259389868.pdf",
                        "name": "hej",
                        "owner": "5a27ce917ae6da0021d97ef4",
                        "path": "/materials/242235471/5a27ce917ae6da0021d97ef4/hej-15125582259389868.pdf",
                        "stars": [
                            {
                                "rate": 5,
                                "username": "815247452"
                            }
                        ],
                        "votes": 1
                    }
                ],
                "name": "Toaster from test with pdf",
                "producer": "242235471",
                "productNo": "242235471"
            }
        },
        "message": "Found product",
        "status": 200
    }

#### Get all products for a company
https://nanotu.be/companies/<name>/products | GET
Returns all the listed products of the specified company as the following JSON:


    {
        "data": {
            "products": [
                {
                    "_id": "5a201b3be32148027dfa18dd",
                    "category": "super_awesome_cars",
                    "createdBy": "ElonMusk",
                    "description": "en gul bil",
                    "files": [],
                    "name": "gul bil",
                    "producer": "tesla",
                    "productNo": "123333"
                },
                {
                    "_id": "5a202ddfe3214803f7dc192a",
                    "category": "super_awesome_cars",
                    "createdBy": "ElonMusk",
                    "description": "en blå bil",
                    "files": [
                        {
                            "file": "/materials/tesla/product_id/filename-1512058335748237.pdf"
                        },
                        {
                            "file": "/materials/tesla/product_id/filename-15120583750399292.pdf"
                        }
                    ],
                    "name": "blå bil",
                    "producer": "tesla",
                    "productNo": "1223"
                }
            ]
        },
        "message": "Successfully retreived all the products for company tesla",
        "status": 200
    }

#### Get material
https://nanotu.be/materials/<company>/<product_id>/<filename> | GET
Returns the saved file

#### Rate Material
https://nanotu.be/products/<product_id>/materials/<material_name>/rate | POST
Gives the selected material a rating. Requires the following data:

    "jwt": "a.consumer.jwt",
    "rate": 4 (An integer between 1 and 5)

#### Create Annotations
https://nanotu.be/consumers/<username>/materials/<material_id>/annotations | POST
Creates or updates annotation. If there is already an annotation for the specified material this method will just overwrite it with a new one. Else it creates a new annotation for that material. Requires the following data:

    "username" {string} -- name of user the annotation belongs to
    "material_id" {string} -- id of material to annotate

#### Get Annotations
https://nanotu.be/consumers/<username>/materials/<material_id>/annotations | GET
Gets all annotations connected to a specifi file. Requires the following data:

    "username": "Bertil Hansson"
    "material_id": "filnamnkylskap123"

Returns the following JSON and the statuscode:

    {"data": {
        "annotations": "Litet kylskåp"
            }
    }
    "message": "Successfully retreived the annotations for the material"
    "status": 200

#### Get Threads
https://nanotu.be/threads | GET
Returns the created thread in a list in the following JSON:

[
    {
        "id": "rifsffshfh",
        "name": "Sven",
        "title": "Vad är egentligen ett kylskåp?",
        "timestamp": "typ-nyss"
    },
    {
        "id": "7483302",
        "name": "Jörgen",
        "title": "Varför är lampan röd?",
        "timestamp": "ungefär-nu"
    }
]
Returns the following statuscode:

    "message": "Successfully retrieved all the threads"
    "status": 200

#### Create Thread
https://nanotu.be/threads | POST
Creates a thread reply with text. Returns the id of the created thread. Requires the following data:

    {
        "jwt": "rep.or.consumer",
        "message": "An answer I have"
    }

    "message": "Thread was created" 
    "status": 201

#### Get Thread
https://nanotu.be/threads/<_id> | GET
Returns a single thread for a specific product. Requires the following data:

    {
        "id": "thread.id"
    }
    
Returns the statuscode and located thread:

    "status": 200

#### Create Reply
https://nanotu.be/threads/<_id>/replies | POST
Posts a reply to a specific thread. Requires the following data:

    {
        "jwt": "rep.or.consumer",
        "id": "thread.id"
    }

Returns the the following data:

"message": "Reply created"
"status": 201