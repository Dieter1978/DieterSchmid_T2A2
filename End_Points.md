# API Endpoints Documentation

## Table of Contents

1. [Auth Routes](#auth-routes)
2. [PC Routes](#pc-routes)
3. [Part Routes](#part-routes)
4. [PcBuildPart Routes](#pcbuildpart-routes)

## Auth Routes

### /auth/users

### Method : GET

List all users stored in the database.

- Parameters : None
- Authentication : None
- JWT Token Authorization : Not required

* Request Body: None
* Request response :

```JSON

 [
    {
        "email": "admin@spam.com",
        "is_admin": true,
        "name": null,
        "pcs": [
            {
                "description": "Beast of a machine",
                "name": "The Hog",
                "value": 0.0
            },
            {
                "description": "Stealthy and quiet",
                "name": "The Dart",
                "value": 0.0
            }
        ]
    },
  ]
```

### /auth/users/id

### Method : GET

Gets the user from teh database using the id passed in.

- Authentication : None
- JWT Token Authorization : Not required

- Request Body: None
- Response Body :

```JSON
{
    "email": "admin@spam.com",
    "is_admin": true,
    "name": null,
    "password": "$2b$12$5wMAwkKCarhGW7Q2KkXDQOjosR9TDOhfcAOztwmPEfed3UV82BpCm",
    "pcs": [
        {
            "description": "Beast of a machine",
            "name": "The Hog",
            "value": 0.0
        },
        {
            "description": "Stealthy and quiet",
            "name": "The Dart",
            "value": 0.0
        }
    ]
}

```

### /auth/register

### Methods : POST

Create a new user in the database with encypted password.

- Parameters : None
- Authentication : None

* JWT Token Authorization : Not required

* Request Body

```JSON
{
    "name" :"biffo",
    "email": "spiders@rack.com",
    "password" : "divergent"
}
```

- Response Body

```JSON
{
    "email": "spiders@rack.com",
    "is_admin": false,
    "name": "biffo",
    "pcs": []
}
```

### /auth/login

### Methods : POST

Log user into to system and provide JWT session token.

- Parameters : None
- Authentication : None
- JWT Token Authorization : Not required

- Request Body

```JSON
{
    "email" : "cleese@spam.com",
    "password" : "tisbutascratch"

}
```

- Response Body

```JSON
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NzQwMzAwMSwianRpIjoiMTg1YWMxMTAtOTdjMi00NmEzLWI3NGUtNjI1ZWIxMzBiMDViIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NiwibmJmIjoxNjg3NDAzMDAxLCJleHAiOjE2ODc0ODk0MDF9.hAnjMtXCjgJmGArnTArBBwyGSRkGB2GOzWKN8r4hULU",
    "user": {
        "email": "cleese@spam.com",
        "is_admin": false,
        "name": "John Cleese",
        "pcs": [
            {
                "description": "Gaming",
                "name": "The Beatle",
                "value": 1300.0
            }
        ]
    }
}
```

## PC Routes

### /pcs

### Methods : GET

List all PCs in the database.

- Parameters : None
- Authentication : None
- JWT Token Authorization : Not required

- Request Body : None
- Response Body :

```JSON
[
    {
        "description": "Beast of a machine",
        "id": 7,
        "name": "The Hog",
        "user": {
            "email": "admin@spam.com",
            "is_admin": true,
            "name": null
        },
        "value": 0.0
    },
    {
        "description": "Stealthy and quiet",
        "id": 8,
        "name": "The Dart",
        "user": {
            "email": "admin@spam.com",
            "is_admin": true,
            "name": null
        },
        "value": 0.0
    },
    {
        "description": "Gaming",
        "id": 9,
        "name": "The Beatle",
        "user": {
            "email": "cleese@spam.com",
            "is_admin": false,
            "name": "John Cleese"
        },
        "value": 1300.0
    }
]
```

### /pcs/id

### Methods : GET

Gets an indivudal PC from the database.

- Parameters : pc_id
- Authentication : None
- JWT Token Authorization : Not required

- Request Body : None
- Response Body :

```JSON
{
    "description": "Gaming",
    "id": 9,
    "name": "The Beatle",
    "user": {
        "email": "cleese@spam.com",
        "is_admin": false,
        "name": "John Cleese"
    },
    "value": 1300.0
}
```

### /pcs/

### Methods : POST

Creates a new PC in the database under the user id log in with.

- Parameters : None
- Authentication : Logged in User from the database.
- JWT Token Authorization : Required.

- Request Body

```JSON
{
    "name" : "Fast Larry",
    "description" : "Casual gaming machine - fast",
    "value" : 1000.00
}
```

- Response Body

```JSON
{
    "description": "Casual gaming machine - fast",
    "id": 10,
    "name": "Fast Larry",
    "user": {
        "email": "cleese@spam.com",
        "is_admin": false,
        "name": "John Cleese"
    },
    "value": 1000.0
}
```

### /pcs/id

### Methods : 'PUT' and 'PATCH'

Updates the details of a PC in the database.

- Parameters : pc_id
- Authentication : Logged in User from the database.
- JWT Token Authorization : Required.

- Request Body

```JSON
{
    "description": "Gaming",
    "name": "The Beatle",
    "value": 1300.0
}
```

- Response Body

```JSON
{
    "description": "Gaming",
    "id": 9,
    "name": "The Beatle",
    "user": {
        "email": "cleese@spam.com",
        "is_admin": false,
        "name": "John Cleese"
    },
    "value": 1300.0
}
```

### /pcs/id

### Methods : DELETE

Removes a PC from the database based on id parameter.

- Parameters : pc_id
- Authentication : Logged in User from the database.
- JWT Token Authorization : Required.

- Request Body : None

- Response Body

```JSON
{}
```

## Part Routes

### /parts

### Methods : GET

Returns and displays a list of all parts in the database.

- Parameters : None
- Authentication : None
- JWT Token Authorization : Not required

- Request Body : None
- Response Body :

```JSON
[
    {
        "description": "stick of RAM",
        "id": 11,
        "name": "16GB RAM",
        "value": 100.0
    },
    {
        "description": "stick of RAM",
        "id": 12,
        "name": "32GB RAM",
        "value": 180.0
    },
    {
        "description": "super fast cpu",
        "id": 13,
        "name": "i7 11700KF intel",
        "value": 399.0
    },
]
```

### /parts/id

### Methods : GET

Return a part based on the id passed in.

- Parameters : part_id
- Authentication : None
- JWT Token Authorization : Not required

- Request Body : None
- Response Body

```JSON
{
    "description": "Really really fast CPU",
    "id": 14,
    "name": "Ryzen 9 7950X3D",
    "value": 1000.0
}
```

### /parts

### Methods : POST

Adds a new part to the database.

- Parameters : None
- Authentication : Logged in user
- JWT Token Authorization : required

- Request Body

```JSON
{
    "name" : "GeForce GTX 1650 4GB",
    "description" : "Budget graphics card",
    "value" : 249.00
}
```

- Response Body

```JSON
{
    "description": "Budget graphics card",
    "id": 16,
    "name": "GeForce GTX 1650 4GB",
    "value": 249.0
}
```

### /parts/id

### Methods : 'PATCH' and 'PUT'

Updates the values of a part in the database from the part_id passed in.

- Parameters : part_id
- Authentication : Must be logged in user.
- JWT Token Authorization : Required

- Request Body

```JSON
{
    "name" : "GeForce GTX 1650 8GB",
    "description" : "Budget graphics card",
    "value" : 299.00
}
```

- Response Body

```JSON
{
    "description": "Budget graphics card",
    "id": 16,
    "name": "GeForce GTX 1650 8GB",
    "value": 299.0
}
```

### /parts/id

### Methods : DELETE

Removes a part from the database based on the part_id

- Parameters : part_id
- Authentication : Login in user must be Administrator
- JWT Token Authorization : Required

- Request Body : None
- Response Body

```JSON
{}
```

## PcBuildPart Routes

### /pcs/<pc_id>/pcbuild

### Methods : GET

Returns and displays Pc build parts in the database

- Parameters : None
- Authentication : User must be logged in
- JWT Token Authorization : Required

- Request Body : None
- Response Body

```JSON
[
    {
        "number": null,
        "part": {
            "description": "stick of RAM",
            "name": "16GB RAM"
        },
        "part_id": 11,
        "pc": {
            "name": "The Hog"
        },
        "value": null
    },
    {
        "number": null,
        "part": {
            "description": "super fast cpu",
            "name": "i7 11700KF intel"
        },
        "part_id": 13,
        "pc": {
            "name": "The Hog"
        },
        "value": null
    },
    {
        "number": null,
        "part": {
            "description": "12GB super fast graphics card",
            "name": "GeForce RTX 3060"
        },
        "part_id": 15,
        "pc": {
            "name": "The Hog"
        },
        "value": null
    }
]
```

### /pcs/<pc_id>/pcbuild

### Methods : POST

Creates a new part of the PC build and adds it the pc build part in the database.

- Parameters : pc_id
- Authentication : User must be logged in
- JWT Token Authorization : Required

- Request Body

```JSON
{
    "number" : 1,
    "value" : 0,
    "part_id" : 15

}
```

- Response Body

```JSON
{
    "description": "Beast of a machine",
    "id": 7,
    "name": "The Hog",
    "user": {
        "email": "admin@spam.com",
        "is_admin": true,
        "name": null
    },
    "value": 0.0
}
```

### /pcs/<pc_id>/pcbuild/<pcbuild_id>/

### Methods : PUT and PATCH

Updates a PC build part in the database.

- Parameters : pc_id, pcbuild_id
- Authentication : User must be logged in
- JWT Token Authorization : Required

- Body request

```JSON
{
    "number" : 1,
    "value" : 500,
    "part_id" : 15

}
```

- Response body

```JSON
{
    "description": "Beast of a machine",
    "id": 7,
    "name": "The Hog",
    "user": {
        "email": "admin@spam.com",
        "is_admin": true,
        "name": null
    },
    "value": 0.0
}
```

### /pcs/<pc_id>/pcbuild/<pcbuild_id>/

### Methods : DELETE

Removes a pcbuild part from the pc and database.

- Parameters : pc_id, pcbuild_id
- Authentication : Admin or User must be logged in
- JWT Token Authorization : Required

- Body request : none
- Body response

```JSON
{}
```
