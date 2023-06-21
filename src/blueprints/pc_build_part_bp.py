from flask import Blueprint, request, abort, jsonify
from models.pc import Pc, PcSchema
from models.user import User, UserSchema
from models.part import Part, PartSchema
from models.pc_build_part import Pc_Build_Part, Pc_Build_PartSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, admin_or_owner_required
from datetime import date

pc_build_part_bp = Blueprint('comments', __name__)


@pc_build_part_bp.route('/pcs/<int:id>/pcbuild')
def show_build(id):
    #Create a statement to get all the pc build parts based on the id from the route
    stmt = db.select(Pc_Build_Part).where(Pc_Build_Part.pc_id == id)
    #execute the statement which returns all the pc build parts
    pcbuild = db.session.scalars(stmt).all()   
    return Pc_Build_PartSchema(many=True).dump(pcbuild)

@pc_build_part_bp.route('/pcs/<int:pc_id>/pcbuild', methods=['POST'])
@jwt_required()
def create_build_part(pc_id):
    pcbuild_fields = Pc_Build_PartSchema().load(request.json)
    # get the user id invoking get_jwt_identity
    #user_id = get_jwt_identity()
    #Find it in the db
    #user = User.query.get(user_id)
    # Make sure it is in the database
    ##   return abort(401, description="Invalid user")

    # execute a query that returns the pc id from the route
    pc = Pc.query.filter_by(id=pc_id).first()
    # return an error if the card doesn't exist
    if not pc:
        return abort(400, description="Pc does not exist")
    # create the pc build part with the given values
    new_PcBuildPart = Pc_Build_Part()
    new_PcBuildPart.number = pcbuild_fields["number"]
    new_PcBuildPart.value = pcbuild_fields["value"]
    new_PcBuildPart.part_id = pcbuild_fields["part_id"]
    # Use the pc gotten by the id of the route
    new_PcBuildPart.pc = pc
    
   
    # add to the database and commit
    db.session.add(new_PcBuildPart)
    #write to the database
    db.session.commit()

    # return the Pc in the response
    return PcSchema().dump(pc), 201  

@pc_build_part_bp.route("/pcs/<int:pc_id>/pcbuild/<int:pcbuild_id>", methods=['PUT', 'PATCH'])
@jwt_required()
def update_pcbuild(pc_id, pcbuild_id):

    #create a statement to get the pc build part id from the route
    stmt = db.select(Pc_Build_Part).filter_by(id=pcbuild_id)
    #execute the statement and return the pcbuild part
    pcbuild = db.session.scalar(stmt)

    if pcbuild is not None:
        #execute a query to get the pc id from the route
        pc = Pc.query.filter_by(id=pc_id).first()
        admin_or_owner_required(pc.user.id)
        pcbuild_fields = Pc_Build_PartSchema().load(request.json)
        #update the pc build part with the value passed in by the JSON
        pcbuild.number = pcbuild_fields.get('number', pcbuild.number)
        pcbuild.value = pcbuild_fields.get('value', pcbuild.value)
        pcbuild.part_id = pcbuild_fields.get('part_id', pcbuild.part_id)
        # model has been changed now commit the update
        db.session.commit()
        
        return PcSchema().dump(pc), 202
    else:
        # no card comes back with 404 Not Found
        return {"Error": "No Pc with this id was found"}, 404


# Delete a Pc Build Part instance
@pc_build_part_bp.route("/pcs/<int:pc_id>/pcbuild/<int:pcbuild_id>", methods=['DELETE'])
@jwt_required()
def delete_card(pc_id, pcbuild_id):
    #create a query to get the pc build part based on the id from the route
    stmt = db.select(Pc_Build_Part).filter_by(id=pcbuild_id)
    #execute the query and get the pc build part
    pcbuild = db.session.scalar(stmt)
    if pcbuild:
        #use a query to get the pc passed in by the route id
        pc = Pc.query.filter_by(id=pc_id).first()
        admin_or_owner_required(pc.user.id)
        #add pc build part for deletion
        db.session.delete(pcbuild)
        #do the delete
        db.session.commit()
        return {}, 200
    else:
        return {"Error": "No Pc with this id was found"}, 404
