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