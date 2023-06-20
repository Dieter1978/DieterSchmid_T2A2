from flask import Blueprint, request, abort
from models.part import Part, PartSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, admin_or_owner_required


parts_bp = Blueprint('parts', __name__, url_prefix='/parts')

@parts_bp.route("/")
def all_pcs():
    ''' List all PCs in the database

        Returns :
        Serialized JSON representation of Pc data.
    
    '''
    stmt = db.select(Part)
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

    stmt = db.select(Part).filter_by(id=part_id)
    part = db.session.scalar(stmt)
    if part is not None:
        return PartSchema().dump(part)
    else:
        # no pc comes back with 404 Not Found
        return {"Error": "No part with this id was found"}, 404

@parts_bp.route('/', methods=['POST'])
def create_part():
    ''' Creates new Part in database by loading JSON data passed via web POST request
    
        Returns :
        Serialized JSON representation of Part data.
    
    '''
    part_info = PartSchema().load(request.json)
    part = Part(
        name=part_info['name'],
        description=part_info['description'],
        value=part_info['value']
        
    )
    db.session.add(part)
    db.session.commit()
    return PartSchema().dump(part), 201


# Update a PC
@parts_bp.route('/<int:part_id>', methods=['PUT', 'PATCH'])
def update_part(part_id):
    ''' Update the fields of a Part already in the database, from JSON passed via a web PUT or PATCH request
    
        Returns :
        Serialized JSON representation of Part data.
    
    '''
    stmt = db.select(Part).filter_by(id=part_id)
    part = db.session.scalar(stmt)
    if part is not None:
        #admin_or_owner_required(pc.user.id)
        part_info = PartSchema().load(request.json)

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
def delete_part(part_id):
    ''' Delete a Part from the database based on the id passed in.
    
        Parameters:
        argument1 (int) : part_id

        Returns :
        Empty JSON object

    '''
    stmt = db.select(Part).filter_by(id=part_id)
    part = db.session.scalar(stmt)
    if part:
        #admin_or_owner_required(part.user.id)
        db.session.delete(part)
        db.session.commit()
        return {}, 200
    else:
        return {"Error": "No part with this id was found"}, 404