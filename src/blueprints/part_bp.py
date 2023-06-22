from flask import Blueprint, request, abort
from models.part import Part, PartSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, admin_or_owner_required


parts_bp = Blueprint('parts', __name__, url_prefix='/parts')

@parts_bp.route("/")
def all_parts():
    ''' List all Parts in the database

        Returns :
        Serialized JSON representation of Pc data.
    
    '''
    # create an SQL statement to get all parts from the database
    stmt = db.select(Part)
    # execute the statement which return all parts from the database
    parts = db.session.scalars(stmt).all()
    return PartSchema(many=True).dump(parts)

@parts_bp.route('/<int:part_id>')
def one_part(part_id):
    ''' List a Part in the database

        Parameters:
        argument1 (int) : part_id

        Returns :
        Serialized JSON representation of Part data.
    
    '''
    # create an SQL statement a part from the database based on the route id
    stmt = db.select(Part).filter_by(id=part_id)
    #execute the statement which returns the part fromt the database
    part = db.session.scalar(stmt)
    if part is not None:
        return PartSchema().dump(part)
    else:
        # no pc comes back with 404 Not Found
        return {"Error": "No part with this id was found"}, 404

@parts_bp.route('/', methods=['POST'])
@jwt_required()
def create_part():
    ''' Creates new Part in database by loading JSON data passed via web POST request
    
        Returns :
        Serialized JSON representation of Part data.
    
    '''
    part_info = PartSchema().load(request.json)
    #create a new instance of Part model
    part = Part(
        name=part_info['name'],
        description=part_info['description'],
        value=part_info['value']
        
    )
    #add the intance to the database session
    db.session.add(part)
    #write the Part data to the database
    db.session.commit()
    return PartSchema().dump(part), 201


# Update a PC
@parts_bp.route('/<int:part_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_part(part_id):
    ''' Update the fields of a Part already in the database, from JSON passed via a web PUT or PATCH request
    
        Returns :
        Serialized JSON representation of Part data.
    
    '''
    #create a statement to select a part based on the id from the route
    stmt = db.select(Part).filter_by(id=part_id)
    #execute the statement store the return the part
    part = db.session.scalar(stmt)
    if part is not None:
        #admin_required()
        part_info = PartSchema().load(request.json)
        #update the part value from the JSON data passed in
        part.name = part_info.get('name', part.name),
        part.description = part_info.get('description', part.description),
        part.value = part_info.get('value', part.value),
        # model has been changed now commit the update
        db.session.commit()
        return PartSchema().dump(part), 202
    else:
        # no card comes back with 404 Not Found
        return {"Error": "No part with this id was found"}, 404
    

# Delete a card
@parts_bp.route('/<int:part_id>', methods=['DELETE'])
@jwt_required()
def delete_part(part_id):
    ''' Delete a Part from the database based on the id passed in.
    
        Parameters:
        argument1 (int) : part_id

        Returns :
        Empty JSON object

    '''
     #create a statement to select a part based on the id from the route
    stmt = db.select(Part).filter_by(id=part_id)
    #execute the statement store the return the part
    part = db.session.scalar(stmt)
    if part:
        admin_required()
        #add the part for deletion
        db.session.delete(part)
        #delete the part from the database
        db.session.commit()
        return {}, 200
    else:
        return {"Error": "No part with this id was found"}, 404