from flask import Blueprint, request, abort
from models.user import User, UserSchema
from init import db, bcrypt
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

auth_bp = Blueprint('auth', __name__)


def admin_required():
    #extract the user id from the token
    user_id = get_jwt_identity()
    #create query to select user based on token id
    stmt = db.select(User).filter_by(id=user_id)
    #execute the query and get the user
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        # Unauthorised
        abort(401, description="Unauthorized, Admin access required")


def admin_or_owner_required(owner_id):
    #extract the user id from the token
    user_id = get_jwt_identity()
    #create query to select user based on token id
    stmt = db.select(User).filter_by(id=user_id)
    #execute the query and get the user
    user = db.session.scalar(stmt)
    if not (user and (user.is_admin or user_id == owner_id)):
        # Unauthorised
        abort(401, description="Unauthorized, Admin or owner access required")


@auth_bp.route('/auth/users')
def all_users():
    #create query to get all users in the system
    stmt = db.select(User)
    #execute the query and return to users
    users = db.session.scalars(stmt)
    #display in JSON
    return UserSchema(many=True, exclude=['password']).dump(users)

@auth_bp.route('/auth/users/<int:user_id>')
def one_user(user_id):
    ''' List a User in the database

        Parameters:
        argument1 (int) : user_id

        Returns :
        Serialized JSON representation of user data.
    
    '''
    # setup a statement to select a user by the id passed from the route
    stmt = db.select(User).filter_by(id=user_id)
    # execute the statement and store the returned user data
    user = db.session.scalar(stmt)
    if user is not None:
        return UserSchema().dump(user)
    else:
        # no pc comes back with 404 Not Found
        return {"Error": "No user with this id was found"}, 404


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        user_info = UserSchema().load(request.json)
        #create user instance with JSON passed in
        user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(
                user_info['password']).decode('utf8'),
            name=user_info['name']
        )
        #add instance of user to database session
        db.session.add(user)
        #write user to database
        db.session.commit()
        #display user in JSON
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        #create query to select user based on email address
        stmt = db.select(User).filter_by(email=request.json['email'])
        #execute query and return user
        user = db.session.scalar(stmt)
        #test from user and password
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(
                identity=user.id, expires_delta=timedelta(days=1))
            #return JSON user data with Token information
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400
