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
    stmt = db.select(Pc)
    pcs = db.session.scalars(stmt).all()
    return PcSchema(many=True).dump(pcs)

@pcs_bp.route('/<int:pc_id>')
def one_pc(pc_id):
    ''' List a PC in the database

        Parameters:
        argument1 (int) : pc_id

        Returns :
        Serialized JSON representation of Pc data.
    
    '''

    stmt = db.select(Pc).filter_by(id=pc_id)
    pc = db.session.scalar(stmt)
    if pc is not None:
        return PcSchema().dump(pc)
    else:
        # no pc comes back with 404 Not Found
        return {"Error": "No pc with this id was found"}, 404

@pcs_bp.route('/', methods=['POST'])
def create_pc():
    ''' Creates new PC in database by loading JSON data passed via web POST request
    
        Returns :
        Serialized JSON representation of Pc data.
    
    '''
    pc_info = PcSchema().load(request.json)
    pc = Pc(
        name=pc_info['name'],
        description=pc_info['description'],
        value=pc_info['value'],
        user_id=get_jwt_identity()
    )
    db.session.add(pc)
    db.session.commit()
    return PcSchema().dump(pc), 201


# Update a PC
@pcs_bp.route('/<int:pc_id>', methods=['PUT', 'PATCH'])
def update_card(pc_id):
    ''' Update the fields of a PC already in the database, from JSON passed via a web PUT or PATCH request
    
        Returns :
        Serialized JSON representation of Pc data.
    
    '''
    stmt = db.select(Pc).filter_by(id=pc_id)
    pc = db.session.scalar(stmt)
    if pc is not None:
        #admin_or_owner_required(pc.user.id)
        pc_info = PcSchema().load(request.json)

        pc.name = pc_info.get('name', pc.name),
        pc.description = pc_info.get('description', pc.description),
        pc.value = pc_info.get('value', pc.value),
        # model has been changed now commit the update
        db.session.commit()
        return PcSchema().dump(pc), 202
    else:
        # no card comes back with 404 Not Found
        return {"Error": "No pc with this id was found"}, 404
    

# Delete a card
@pcs_bp.route('/<int:pc_id>', methods=['DELETE'])
def delete_pc(pc_id):
    ''' Delete a PC from the database based on the id passed in.
    
        Parameters:
        argument1 (int) : pc_id

        Returns :
        Empty JSON object

    '''
    stmt = db.select(Pc).filter_by(id=pc_id)
    pc = db.session.scalar(stmt)
    if pc:
        admin_or_owner_required(pc.user.id)
        db.session.delete(pc)
        db.session.commit()
        return {}, 200
    else:
        return {"Error": "No pc with this id was found"}, 404