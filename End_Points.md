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
