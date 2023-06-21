from flask import Blueprint, request, abort
from models.pc import Pc, PcSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, admin_or_owner_required
from datetime import date

pcs_bp = Blueprint('pcs', __name__, url_prefix='/pcs')

@pcs_bp.route("/")
def all_pcs():
    ''' List all PCs in the database

        Returns :
        Serialized JSON representation of Pc data.
    
    '''
    #setup a select statement to get all the PCs from the database
    stmt = db.select(Pc)
    #execute the statement and return all Pcs in the database data to pcs
    pcs = db.session.scalars(stmt).all()
    #display the data using JSON
    return PcSchema(many=True).dump(pcs)

@pcs_bp.route('/<int:pc_id>')
def one_pc(pc_id):
    ''' List a PC in the database

        Parameters:
        argument1 (int) : pc_id

        Returns :
        Serialized JSON representation of Pc data.
    
    '''
    # setup a statement to select a Pc by the id passed from the route
    stmt = db.select(Pc).filter_by(id=pc_id)
    # execute the statement and store the returned pc data
    pc = db.session.scalar(stmt)
    if pc is not None:
        return PcSchema().dump(pc)
    else:
        # no pc comes back with 404 Not Found
        return {"Error": "No pc with this id was found"}, 404

@pcs_bp.route('/', methods=['POST'])
@jwt_required()
def create_pc():
    ''' Creates new PC in database by loading JSON data passed via web POST request
    
        Returns :
        Serialized JSON representation of Pc data.
    
    '''
    pc_info = PcSchema().load(request.json)
    #Create an instane of the Pc model and store the values from the JSON
    pc = Pc(
        name=pc_info['name'],
        description=pc_info['description'],
        value=pc_info['value'],
        user_id=get_jwt_identity()
    )
    #add the new model to the session
    db.session.add(pc)
    #write the Pc data to the database
    db.session.commit()
    return PcSchema().dump(pc), 201


# Update a PC
@pcs_bp.route('/<int:pc_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_card(pc_id):
    ''' Update the fields of a PC already in the database, from JSON passed via a web PUT or PATCH request
    
        Returns :
        Serialized JSON representation of Pc data.
    
    '''
    # setup a statement to select a Pc by the id passed from the route
    stmt = db.select(Pc).filter_by(id=pc_id)
    # execute the statement and store the returned pc data
    pc = db.session.scalar(stmt)
    if pc is not None:
        admin_or_owner_required(pc.user.id)
        #store schema for serialisation
        pc_info = PcSchema().load(request.json)
        #add update value to the PC object.
        pc.name = pc_info.get('name', pc.name),
        pc.description = pc_info.get('description', pc.description),
        pc.value = pc_info.get('value', pc.value),
        # model has been changed now commit the update to the database
        db.session.commit()
        # display the PC data in JSON
        return PcSchema().dump(pc), 202
    else:
        # no card comes back with 404 Not Found
        return {"Error": "No pc with this id was found"}, 404
    

# Delete a card
@pcs_bp.route('/<int:pc_id>', methods=['DELETE'])
@jwt_required()
def delete_pc(pc_id):
    ''' Delete a PC from the database based on the id passed in.
    
        Parameters:
        argument1 (int) : pc_id

        Returns :
        Empty JSON object

    '''
    # setup a statement to select a Pc by the id passed from the route
    stmt = db.select(Pc).filter_by(id=pc_id)
    # execute the statement and store the returned pc data
    pc = db.session.scalar(stmt)
    if pc:
        admin_or_owner_required(pc.user.id)
        #add the pc to the session for deletion
        db.session.delete(pc)
        #make the deletion change in the database
        db.session.commit()
        return {}, 200
    else:
        return {"Error": "No pc with this id was found"}, 404