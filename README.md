# PROJECT DOCUMENTATION

## R1 Identification of the problem you are trying to solve by building this particular app.

The modern PC is made up of many customisable parts. Building a PC requires planning. Often a person will need to compile a list of parts on a spreadsheet or paper then used that to research configuration compatibilities and find quotes. By creating an API application we can make this process easier by storing PC configurations and the list of part.

## R2 Why is it a problem that needs solving?\*\*

Their are number of reasons for doing this. But ultimately we trying to ease the burden on the consumer when shopping for PC parts. although the initial app MVP is just to store configurations as a catalogue of the users PC builds, it could certainly be built to allow :

1. part comparability checks, helping to resolve conflicting hardware issues often encountered after a purchase.
2. Connection to third party apis to provide multiple options and instantaneous pricing for parts.

These two are items whilst not include in todays app are surely for food for thought in creating a seed for a PC building online business model driven by having PC config first rather then scouring the web for the parts one needs.

## R3 Why have you chosen this database system. What are the drawbacks compared to others?\*\*

PostSQL was chooses for three reasons.

1. Constraints on the options available to choose from.
2. It’s an industry standard production level database that is often used to support web applications and is therefore considered a reliable and robust choice.
3. It is low maintenance, easily adminstratored and easy to use.

Their a range of other benefits such as its wide OS compatibility support for all major programming language. It supports SQL and advanced SQL functions as well as non relational JSON. However their are draw backs:

1. Costs associated with migration, support and maintenance. Whilst downloading the software is free. Hiring a consulting practise that specialises in PostgreSQL can be a costly endeavour. Early planning is needed to anticipate such costs.
2. No single vendor control. Moving to PostgreSQL means dealing with multiple vendors. This can get confusing for example their are 5 different backup solutions on the market for PostgreSQL. Approaching multiple vendors for solutions is challenging and again consulting costs might be incurred as external expertise is sought.
3. PostgreSQL has less support across the open source field then MySQL. 4. Important in this day and age is decide weather to have PostgreSQL on premise or in the cloud. The cloud versions of PostgreSQL are most renown in Amazon cloud services. User have found that it can be quiet costly as its resource consumption is quite high. Sometimes users have
   moved back to on-premise solution to control expenses.
4. Finally companies need to work if they have the in-house expertise or if they need it. If not then they are reliant on third party partners or consultants to support the in-house skills. Sometimes a companies
   will hire new expertise in just for helping support PostgreSQL.

## R4 Identify and discuss the key functionalities and benefits of an ORM.\*\*

Object Relational Mapping controls the interact between an application and the database it connects to. By using ORM we do not need to use direct SQL statement to work with data in the database. Instead we can use the programming language the application is being developed in. We can use things like Object Oriented Classes and models as integrated data structures instead of SQL tables. The major benefits of this are :

- Elimantes the need for repetive SQL code. Cleaner and less code. This ultimately speeds up development time.
- Less requirements to understand what going on 'under the hood' are wide variety of tasks are already implemented out of the box.
- Avoid the need for vendor specifc SQL. The ORM already knows which vendor and implements whats nessary so you dont have to worry.
- ORMs also provide some shielding agaisnt things like SQL injections making the code base more secure.
- Because the ORM abstracts the database it is easy to change database systems should one desire.

## R5 Document all endpoints for your API.\*\*

Please see included End_Points.md file for more information.

## R6 An ERD for your app.\*\*

![ERD Diagram for APP](/Resources/PCBuild_ERD.png)

## R7 Detail any third party services that your app will use.\*\*

This application used the Flask framework to create the PC Configuration API. Flask is a lightweight framework which leaves the majority of design and architecture desicions up to the developer. This means much of the additional functionality is added through Python packages. The Python package manager allows us to take a snap shot of the all dependencies which can be found in this file - ![Requirements.txt](/src/requirements.txt)

The key packages that enable the API are :

### SQLAlchemy

As described earlier, SQLAlchemy provides the ORM functionality to the application. It connects to PostgreSQL server and manages all database transactions. It encapsulates most of the code required to query and work with the PostgreSQL database. It also allows us to create models of the relations we are using and make associations between them easily. The models allow us to work with model objects that the database returns based on the queries made.

### Psycopg2

This package is effectively and driver/adapter that SQLAlchemy uses to connect between the Flask application and PostgreSQL. It is needed because SQLALchemy is vendor agonostic when it comes to databases.

### Flask-Marshmallow

Flask marshmallow provides a schema to support the conversion of complex data types. In our application this is for create a JSON representation of the data pulled from the database. It also converta JSON from a web request to be used in the creation or maintaince of model objects in the datbase. Flask-Marshmallow also provides validation tools which can be implemented in its schemas.

### Python-Dotenv

This package allows us to setup and use environment variables in seperate files like .env and .flaskenv. Information we want outside the application for example like passwords and security can be stored in a seperate file and not upload to public repositories like GitHub. Also enironment variables like debugging mode and which port to run the application on can be added to .flaskenv

### Flask-Bcrypt

Flask-Bcrypt is a popular hashing algorithm choice for passwords. It is based on the Blowfish cipher and is made to be slow and delibrately computationally expensive. This is in order to slow down brute force attacks making it more difficult for attackers to guess or crack passwords.

### Flask-JWT-Extended

The Flask_JWT-Extended library is what is used to manage the use of JWT - JSON Web Tokens. During the authorization process a user is assigned a JWT token upon login, this token helps identify and signal to the web server that the JWT token for the user does or doesnt have permission to access certain resources. The token is self-contained, compact and secure and the web application uses a password to access the tokens it distributes. Tokens can also be set for a expiry period in which the user will need to login again if their token expires

## R8 Describe your projects models in terms of the relationships they have with each other.

The PC Configuration API uses as discussed previously an ORM. The structure of the program seperates all database management through the use of models. It is the ORM SQLalchemy that allows interaction with the database to be done in Python and not SQL. Further the integration tool Marshmallow is used with Sqlalchemy to convert data into a format either usable for the database or for the API (JSON). Lets look specifically at the models in the PC Configuration API

### The User Model.

```python
from init import db, ma
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    pcs = db.relationship(
        'Pc', back_populates='user', cascade='all,delete')

class UserSchema(ma.Schema):
    pcs = fields.List(fields.Nested('PcSchema', exclude=['user', 'id']))

    class Meta:
        fields = ('name', 'email', 'password', 'is_admin','pcs')
```

- The main relationship the User model shows is that of one to many PCs. A user can have many PCs.

```python
pcs = db.relationship(
        'Pc', back_populates='user', cascade='all,delete')
```

### The PC model.

```python
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And, Regexp

class Pc(db.Model):
    __tablename__="pcs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    value = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='pcs')

    pc_build_parts = db.relationship(
        'Pc_Build_Part', back_populates='pc', cascade='all,delete')

class PcSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=[
                         'password', 'pcs'])

    name = fields.String(required=True, validate=And(
        Length(min=5, error='Title must be at least 3 characters long'),
        error='Must be 5 characters long'))

    description = fields.String(load_default='')

    value = fields.Float(load_default=0)


    class Meta:
        fields = ('id', 'name', 'description', 'value','user')
        ordered = True
```

- The relationship here show that a User must own a PC.

```python
user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
user = db.relationship('User', back_populates='pcs')
```

- Also there is a relationship where a PC is made of PC Build Parts.

```python
pc_build_parts = db.relationship(
        'Pc_Build_Part', back_populates='pc', cascade='all,delete')
```

### The Part Model

```python
from init import db, ma
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow import fields

class Part(db.Model):
    __tablename__="parts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    value = db.Column(db.Float)

    pc_build_parts = db.relationship(
        'Pc_Build_Part', back_populates='part', cascade='all,delete')

class PartSchema(ma.Schema):
    name = fields.String(required=True, validate=And(
        Length(min=5, error='Title must be at least 3 characters long'),
        error='Must be 5 characters long'))

    description = fields.String(load_default='')

    value = fields.Float(load_default=0)

    class Meta:
        fields = ('id', 'name', 'description', 'value')
```

- The relationship here is that Part can be part of a PC BUild.

```python
 pc_build_parts = db.relationship(
        'Pc_Build_Part', back_populates='part', cascade='all,delete')
```

### The PC BUild Part model

```python
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And, Regexp

class Pc_Build_Part(db.Model):
    __tablename__ = 'pc_build_parts'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    value = db.Column(db.Float)

    pc_id = db.Column(db.Integer, db.ForeignKey(
        'pcs.id', ondelete='CASCADE'), nullable=False)

    part_id = db.Column(db.Integer, db.ForeignKey(
        'parts.id', ondelete='CASCADE'), nullable=False)

    pc = db.relationship('Pc', back_populates='pc_build_parts')
    part = db.relationship('Part', back_populates='pc_build_parts')

class Pc_Build_PartSchema(ma.Schema):
    pc = fields.Nested('PcSchema', only=['name'])
    part = fields.Nested('PartSchema',only=['name','description'])

    number = fields.Integer(load_default=1)

    value = fields.Float(load_default=0)

    part_id = fields.Integer(required=True)

    class Meta:
        fields = ('number','value','part_id','part','pc')
        ordered = True
```

- A PC Build Part must belong to a PC.

```python
pc_id = db.Column(db.Integer, db.ForeignKey(
        'pcs.id', ondelete='CASCADE'), nullable=False)

pc = db.relationship('Pc', back_populates='pc_build_parts')

```

- A PC Build Part must have a Part associated to it.

```python
part_id = db.Column(db.Integer, db.ForeignKey(
        'parts.id', ondelete='CASCADE'), nullable=False)

part = db.relationship('Part', back_populates='pc_build_parts')
```

## R9 Discuss the database relations to be implemented in your application.

The PC Configuration API is made up of four tables. R6 has a diagram of Enitity relations showing how each of these tables relates to one another. In the previous question the code is shown as to how the relationships between entities is built in the program. Lets examine the relations or tables used.

- Table Users :

Users (id Integer not null primary key, name varchar(100), email not null unique varchar(150), isAdmin boolean )

The Users table is constructed with one primary key it must be unique and it cannot be empty. Uers have a name and email they use to login with the email field cannot be empty and you cannot have two of the same emails in the database. The isAdmin field can be flagged to true or false depending on if the user is setup as an admin for the site. Admins are able to create and delete entities in the database.

- Table PCs :

Pcs (id Integer not null unique primary key, name varchar(100), description text, value float, user_id Integer not null unique foreign key)

The pcs table has a unique primary key but it also has one foriegn key linking it to the user that created the PC.From the ERD diagram we can see that PCs have one User but a User can create many PCs. The other fields name and desccription are self explanitory. The value field represents the total value of the PC and its parts.

- Table Parts :

Parts (id Integer not null unique primary key, name varchar(100), description text, value float)

The Parts table uses a unique primary key identifying each part. The Parts are essentially what are used to be put in a PC Build. They have name a description and each part can have a value represent by a decimal number.

- Table PC_Build_Parts :

PC_Build_Parts (id Integer not null unique primary key, pc_id Integer not null unique foreign key, part_id integer not null unique foreign key, number Integer, value float)

The PC_Build_Parts table has a relationship with Parts and PC and includes foreign keys linking to those tables. If we look on the ERD diagram we can see that a PC can have multiple PC Build Parts and a Part can be in multiple PC Builds Parts. A PC Build Part can be in only one PC and comprise of only one type of part. The PC Build Part may include more then one of the self type of parts represented by the number column. The value of the PC Build Part is also included as a decimal number.

## R10 Describe the way tasks are allocated and tracked in your project.

This project was managing using the Agile methodology. Agile project management focuses on iteration and breaks large project up into smaller parts. As project has a number of tasks and quite a lot of documentation to be track and managed agile seems appropriate. Two techniques were used sprints, a kanban board and stand ups. Their was really only one user story which can be described as :

- A person wants to build a PC with parts that they have selected.

This user story is what the whole app is built around.

Stand ups were conducted online and provided a way to see what other people were achieving, struggling with and planning to do.

Sprints usually involve a scrum team, but this project is a individual assignment so the project mostly involved making to-do lists for each sprint iteration of the development cycle. The sprint cycle consisted of :

- setup and configuration
- models
- blueprints
- validation

The to-do lists for each cycle were tracked using a Trello Kanban board divided into four sections the setup, documentation, In progress and Completed.

[Link to Trello Board] (https://trello.com/b/kipfk3xF/pc-build-configurator)

![Trello](/Resources/trello.png)
